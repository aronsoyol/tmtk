
# coding: utf-8

"""[summary]
mowu (Mongolian Word Unifier)
"""


import array
import json
import os
import sys
from collections import defaultdict

import freetype
import gi
import imagehash
import numpy
from gi.repository import GLib
gi.require_version('HarfBuzz', '0.0')

from gi.repository import HarfBuzz as hb
from PIL import Image
from tqdm import tqdm


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


def get_default_glyph_sub_table():
    return {
        213:  (212, 212),
        236:  (210, 239),
        241:  (242, 242),
        246:  (210, 248),
        270:  (210, 248, 239),
        273:  (248, 239),
        687:  (248, 212)
    }


class Unifier():
    
    __hash_to_id_dict = defaultdict(lambda: list())
    __gid_to_uniq_gid = dict()

    def __init__(self, font_path=""):
        if not font_path:
            this_dir, this_filename = os.path.split(__file__)
            self.__font_path = os.path.join(
                this_dir,
                "MongolianWhite3.ttf"
            )
        else:
            self.__font_path = font_path

        assert os.path.isfile(self.__font_path)

        self.__ft_face = freetype.Face(self.__font_path)
        self.__ft_face.set_char_size(48 * 64)

        self.__render_all_glyphs()
        self.__glyph_sub_table = get_default_glyph_sub_table()
        self.__shaper = Shaper(self.__font_path)

    def __get_font_path(self):
        return self.__font_path

    def render_glyph(self, gid):
        self.__ft_face.load_glyph(gid)

        bitmap = self.__ft_face.glyph.bitmap
        if len(bitmap.buffer) == 0:
            return None

        arr = numpy.array([255 - dot for dot in bitmap.buffer]
                          ).reshape((bitmap.rows, bitmap.width))
        return arr

    def __render_all_glyphs(self):
        hdict = {}

        for n in range(self.__ft_face.num_glyphs):
            arr = self.render_glyph(n)

            if arr is not None:
                img = Image.fromarray(numpy.uint8(arr))
                if img:
                    hs = str(imagehash.phash(img))
                    hdict[n] = hs

        for g_id, hs in sorted(hdict.items(), key=lambda a: a[1]):
            self.__hash_to_id_dict[hs].append(g_id)

        for gls in self.__hash_to_id_dict.values():
            for gid in gls:
                self.__gid_to_uniq_gid[gid] = gls[0]

    def glyph_decompositoin(self, g_lst):
        ls = []
        for g in g_lst:
            if g in self.__glyph_sub_table:
                ls.extend(self.__glyph_sub_table[g])
            else:
                ls.append(g)
        return ls

    def render(self, text):
        pass

    def shape(self, text):
        return self.__shaper.shape(text)

    def get_uniq_gid_list(self, word):
        g_lst = self.shape(word)
        ls = []
        for g in g_lst:
            if g in self.__gid_to_uniq_gid:
                ls.append(self.__gid_to_uniq_gid[g])
        return self.glyph_decompositoin(ls)


    # def unify_corpus(self):
        



def main():
    unifier = Unifier()
    data_set = []
    with open("/Users/aron/dev/workspace/topic_model/qinggis_train_data_0.json", "r") as json_file_0:
        for line in json_file_0:
            data = json.loads(line.strip())
            data_set.append(data)

    token_set = set()

    gid_to_word = defaultdict(lambda: list())
    for data in tqdm(data_set):
        for token in data["token"]:
            # gid_list = unifier.get_uniq_gid_list(token)
            token_set.add(token)
            # gid_to_word[json.dumps(gid_list)] += token

    for token in tqdm(token_set):
        gid_list = unifier.get_uniq_gid_list(token)
        gid_to_word[json.dumps(gid_list)].append(token)


if __name__ == '__main__':
    main()
