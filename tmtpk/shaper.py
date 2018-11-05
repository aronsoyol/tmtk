import sys
import os

import array
import gi
from gi.repository import GLib
gi.require_version('HarfBuzz', '0.0')
from gi.repository import HarfBuzz as hb


class Shaper():

    def __init__(self, font_path):
        try:
            assert os.path.isfile(font_path)
            print(font_path)
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

