
# coding: utf-8

"""[summary]
mowu (Mongolian Word Unifier)
"""

import warnings
import json
import os
import re

from collections import defaultdict

from .__shaper2 import Shaper2 as Shaper
# from . import shaper
import freetype
import imagehash
import numpy

from PIL import Image


MONGOLIAN_PUNCTUATIONS = [chr(w) for w in range(0x1800, 0x180a)]
MONGOLIAN_DIGISTS = [chr(w) for w in range(0x1810, 0x181a)]
MONGOLIAN_CONTROL_CHAR = [chr(w) for w in range(
    0x180b, 0x180f)] + ["\u200c", "\u200d", "\u202f"]
MONGOLIAN_WORD_CHAR = [chr(a) for a in range(
    0x1820, 0x18ab)] + MONGOLIAN_CONTROL_CHAR


try:
    unicode
except NameError:
    unicode = str


def get_default_glyph_decompositoin_table():
    return {
        213:  (212, 212),
        236:  (210, 239),
        241:  (239, 239),
        246:  (210, 248),
        266:  (247, 250),
        270:  (210, 248, 239),
        273:  (248, 239),
        687:  (248, 212),
        699:  (248, 214)

    }


class MenkUnifier():

    def __init__(self, *args, **kwargs):
        this_dir, this_filename = os.path.split(__file__)
        menk_data_path = os.path.join(this_dir, "menk_data.json")
        with open(menk_data_path, "r") as json_file:
            data = json.load(json_file)
            self.composite_table = data["composite"]
            self.substitute_table = data["substitute"]

        return super().__init__(*args, **kwargs)

    def unique(self, word):
        ls = list()
        for ch in word:
            sub = self.substitute_table.get(ch, ch)
            com = self.composite_table.get(sub, sub)
            ls.append(com)
        return "".join(ls)


class Unifier():

    __hash_to_id_dict = defaultdict(lambda: list())
    __gid_to_uniq_gid = dict()
    __gid_2_hash = dict()

    def __init__(self, font_path=""):
        if not font_path:
            this_dir, this_filename = os.path.split(__file__)
            self.__font_path = os.path.join(
                this_dir,
                "MongolianWhite.ttf"
            )
        else:
            self.__font_path = font_path

        assert os.path.isfile(self.__font_path)

        self.__ft_face = freetype.Face(self.__font_path)
        self.__ft_face.set_char_size(48 * 64)

        font_name = os.path.basename(self.__font_path).replace(".", "_")
        self.__render_all_glyphs(font_name)
        self.__glyph_decompositoin_table = \
            get_default_glyph_decompositoin_table()
        self.__shaper = Shaper()

    def set_glyph_decompositoin_table(self, table):
        self.__glyph_decompositoin_table = table

    def get_glyph_decompositoin_table(self):
        return get_default_glyph_decompositoin_table()

    def __get_font_path(self):
        return self.__font_path

    def render_glyph(self, gid):
        self.__ft_face.load_glyph(gid)

        bitmap = self.__ft_face.glyph.bitmap
        if len(bitmap.buffer) == 0:
            return None

        arr = numpy.array(
            [255 - dot for dot in bitmap.buffer]
                          ).reshape((bitmap.rows, bitmap.width))
        return arr

    def draw_glyph(self, gid):
        try:
            return Image.fromarray(
                numpy.uint8(
                    self.render_glyph(gid)))
        except Exception:
            return None

    def show_unicode(word):
        return [hex(ord(w)) for w in word]

    def __render_all_glyphs(self, font_name=""):

        # self.__glyph_hash_table = {}
        gid_2_hash_file = "gid_2_hash_%s.json"%(font_name)
        this_dir, this_filename = os.path.split(__file__)

        gid_2_hash_file_path = os.path.join(
                this_dir,
                gid_2_hash_file
            )

        if os.path.isfile(gid_2_hash_file_path):
            with open(gid_2_hash_file_path, "r") as file:
                self.__gid_2_hash = json.load(file)
        else:
            for n in range(self.__ft_face.num_glyphs):
                img = self.draw_glyph(n)
                if img:
                    hs = str(imagehash.phash(img))
                    self.__gid_2_hash[n] = hs
            with open(gid_2_hash_file_path, "w") as file:
                json.dump(self.__gid_2_hash, fp=file, indent=2)

        for g_id, hs in self.__gid_2_hash.items():
            self.__hash_to_id_dict[hs].append(int(g_id))

        for gls in self.__hash_to_id_dict.values():
            # 选择最小的ID进行统一
            min_id = min(gls)
            for gid in gls:
                self.__gid_to_uniq_gid[gid] = min_id

    def glyph_decompositoin(self, g_lst):
        ls = []
        for g in g_lst:
            if g in self.__glyph_decompositoin_table:
                ls.extend(self.__glyph_decompositoin_table[g])
            else:
                ls.append(g)
        return ls

    def render(self, text):
        pass

    def shape(self, text):
        return self.__shaper.shape(text)

    def get_garray(self, word, ii_to_i=True):

        if ii_to_i:
            word = re.sub("\u1822+", "\u1822", word)

        # '0x182c', '0x180b' = '0x182d'
        # h + \u180b = g
        # monh\u180bvl 和 mongol 字形有一点区别，
        # 应该按照一样的东西来看待，虽然根本就写错了
        word = re.sub("\u182c\u180b", "\u182d", word)

        g_lst = None

        g_lst = self.shape(word)

        ls = []
        for g in g_lst:
            if g in self.__gid_to_uniq_gid:
                ls.append(self.__gid_to_uniq_gid[g])
        return self.glyph_decompositoin(ls)

    def unique(self, word, ii_to_i=True):
        garray = self.get_garray(word, ii_to_i=True)
        return "".join([chr(0xf000 + g) for g in garray])

    def get_gid_to_uniq_gid(self):
        return self.__gid_to_uniq_gid
