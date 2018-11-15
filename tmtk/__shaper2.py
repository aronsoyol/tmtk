from .__utils import harfbuzz as hb
from .__utils.harfbuzz import HARFBUZZ as HB
from .__utils import qahirah as qah
import os

ft = qah.get_ft_lib()

this_dir, this_filename = os.path.split(__file__)

font_path = os.path.join(
    this_dir,
    "MongolianWhite3.ttf"
)

# ft_face = ft.new_face(font_path)
ft_face = ft.new_face(font_path)

# assert isinstance(ft_face, hb.Face)
ft_face.set_char_size(size=1, resolution=qah.base_dpi)

hb_font = hb.Font.ft_create(ft_face)


class Shaper2():
    def __init__(self, font_path=""):
        pass

    def shape(self, word):
        buf = hb.Buffer.create()
        buf.add_str(word)
        buf.direction = HB.DIRECTION_LTR
        buf.script = HB.SCRIPT_MONGOLIAN
        # buf.guess_segment_properties()
        # print(buf.segment_properties)
        # buf.language = HB.getla
        # buf.flags = HB.BUFFER_FLAG_EOT | HB.BUFFER_FLAG_PRESERVE_DEFAULT_IGNORABLES

        hb.shape(hb_font, buf)
        # buf.get_glyphs
        return [info.codepoint for info in buf.glyph_infos]

# ft = qah.get_ft_lib()
# text_size = 20
# buf = hb.Buffer.create()
# ft_face = ft.find_face(font_family)
# ft_face.set_char_size(size=text_size, resolution=qah.base_dpi)
# hb_font = hb.Font.ft_create(ft_face)
