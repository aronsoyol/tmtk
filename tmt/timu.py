
# coding: utf-8

"""[summary]
mowu (Mongolian Word Unifier)
"""


import array
import json
import os
import re
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


class Shaper():
    def __init__(self, font_path):
        try:
            assert os.path.isfile(font_path)
            fontdata = open(font_path, 'rb').read()

            blob = hb.glib_blob_create(GLib.Bytes.new(fontdata))
            face = hb.face_create(blob, 0)
            del blob
            self.__font = hb.font_create(face)
            upem = hb.face_get_upem(face)
            del face
            hb.font_set_scale(self.__font, upem, upem)
            #hb.ft_font_set_funcs (font)
            hb.ot_font_set_funcs(self.__font)
        except:
            print(font_path)

    def shape(self, text_="abvd", flag=False):
        text = text_
        # Need to create GLib.Bytes explicitly until this bug is fixed:
        # https://bugzilla.gnome.org/show_bug.cgi?id=729541

        buf = hb.buffer_create()

        # class Debugger(object):
        #     def message(self, buf, font, msg, data, _x_what_is_this):
        #         print(msg)
        #         return True
        # debugger = Debugger()
        # hb.buffer_set_message_func (buf, debugger.message, 1, 0)

        ##
        ## Add text to buffer
        ##
        #
        # See https://github.com/harfbuzz/harfbuzz/pull/271
        #
        if flag:
            # If you do not care about cluster values reflecting Python
            # string indices, then this is quickest way to add text to
            # buffer:
            #         void hb_buffer_add_utf8 (hb_buffer_t *buffer,
            #                     const char *text,
            #                     int text_length,
            #                     unsigned int item_offset,
            #                     int item_length);
            hb.buffer_add_utf8(buf, text.encode('utf-8'), 0, -1)
            # Otherwise, then following handles both narrow and wide
            # Python builds:
        elif sys.maxunicode == 0x10FFFF:
            hb.buffer_add_utf32(buf, array.array(
                'I', text.encode('utf-32le')), 0, -1)
        else:
            hb.buffer_add_utf16(buf, array.array(
                'H', text.encode('utf-16le')), 0, -1)

        hb.buffer_guess_segment_properties(buf)

        hb.shape(self.__font, buf, [])
        # del font

        infos = hb.buffer_get_glyph_infos(buf)
        # positions = hb.buffer_get_glyph_positions(buf)

        return [info.codepoint for info in infos]


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


class Tokenizer():
    __ptrn2 = re.compile("(\u202f[^\u202f ]+)")
    __ptrn1 = re.compile("([{0}]+)".format("".join(MONGOLIAN_WORD_CHAR)))

    def tokenize(self, text, split_suffix=False, only_mongolian=True):
        level1 = self.__ptrn1.split(text)
        if only_mongolian:
            level1 = level1[1::2]

        if not split_suffix:
            return level1

        level2 = []
        for item in level1:
            level2_sub = self.__ptrn2.split(item)
            level2 += [item for item in level2_sub if item]
        return level2


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
