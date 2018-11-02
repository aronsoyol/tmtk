
# coding: utf-8

"""[summary]
mowu (Mongolian Word Unifier)
"""


import array
import os
import sys
from collections import defaultdict

import freetype
import gi
import imagehash
import numpy
from gi.repository import GLib
from gi.repository import HarfBuzz as hb
from PIL import Image

gi.require_version('HarfBuzz', '0.0')

__version__=="0.0.1"

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

    def render(self, text_="abvd", flag=False):
        text= text_
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

    #     for info,pos in zip(infos, positions):
    #         gid = info.codepoint
    #         cluster = info.cluster
    #         x_advance = pos.x_advance
    #         x_offset = pos.x_offset
    #         y_offset = pos.y_offset

    #         print("gid %04d=%d@%d,%d+%d" % (gid, cluster, x_advance, x_offset, y_offset))
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


class timu():
    
    __hash_to_id_dict = defaultdict(lambda: list())
    __gid_to_uniq_gid = dict()

    
    def __init__(self, font_path = ""):
        if not font_path:
            this_dir, this_filename = os.path.split(__file__)
            self.__font_path = os.path.join(
                this_dir,
                "MongolianWhite3.ttf"
            )
        else:
            self.__font_path = font_path
        self.__render_all_glyphs()
        self.__glyph_sub_table = get_default_glyph_sub_table()
        self.__shaper = Shaper(self.__font_path)

    def __get_font_path(self):
        return self.__font_path

    def __render_glyph(self, face, gid):
        face.load_glyph(gid)

        bitmap = face.glyph.bitmap
        if len(bitmap.buffer) == 0:
            return None

        arr = numpy.array([255 - dot for dot in bitmap.buffer]
                          ).reshape((bitmap.rows, bitmap.width))
        return arr

    def __render_all_glyphs(self):
        hdict = {}
        face = freetype.Face(self.__font_path)
        face.set_char_size(48 * 64)

        for n in range(face.num_glyphs):
            arr = self.__render_glyph(face, n)

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

    def __glyph_decompositoin(self, g_lst):
        ls = []
        for g in g_lst:
            if g in self.__glyph_sub_table:
                ls.extend(self.__glyph_sub_table[g])
            else:
                ls.append(g)
        return ls

    def get_uniq_gid_list(self, word):
        g_lst = self.__shaper.render(word)
        return g_lst
        ls = []
        for g in g_lst:
            if g in self.__gid_to_uniq_gid:
                ls.append(self.__gid_to_uniq_gid[g])
        return self.__glyph_decompositoin(ls)
