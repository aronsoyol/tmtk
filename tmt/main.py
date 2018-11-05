
# coding: utf-8

# In[15]:


import sys
import os
import math
# import freetype2 as freetype # use Qahirah instance
import qahirah as qah
from qahirah import     CAIRO,     Colour,     Glyph,     Vector
ft = qah.get_ft_lib()
# import fribidi as fb
# from fribidi import \
#     FRIBIDI as FB
import harfbuzz as hb


# In[16]:


text_line = "ᠠᠷᠢᠭᠤᠨᠰᠤᠶᠤᠯ"
base_rtl = False # overall direction of line

# Initial font and buffer setup:

text_size = 36
buf = hb.Buffer.create()
ft_face = ft.find_face("MongolianWhite")
print(ft_face.filename)
ft_face.set_char_size(size = text_size, resolution = qah.base_dpi)
hb_font = hb.Font.ft_create(ft_face)

# Use FriBidi to reorder the line and define the embedding levels, using the
# `ReorderLine` convenience wrapper class provided by PyBidi:

# reordered = fribidi.ReorderLine \
#   (
#     text_line = text_line,
#     base_dir = (FB.PAR_LTR, FB.PAR_RTL)[base_rtl],
#     flags = FRIBIDI.FLAGS_DEFAULT
#   )

# Next, collect the glyphs for each segment/run into a list of Qahirah `Glyphs` objects.
# Note the `Buffer.get_glyphs` convenience method provided by HarfPy:

glyphs = []
# glyph_pos = Vector(0, 0)
# for substr, pos1, pos2, level in reordered.each_embedding_run(vis_order = False) :
#     buf.reset()
#     buf.add_str(substr)
#     buf.guess_segment_properties()
#     hb.shape(hb_font, buf)
#     new_glyphs, end_glyph_pos = buf.get_glyphs(glyph_pos)
#     glyph_pos = end_glyph_pos
#     glyphs.extend(new_glyphs)
#end for

# Do the Cairo font setup, and figure out how big an `ImageSurface` we need:


# In[19]:


glyphs = []
glyph_pos = Vector(0, 0)
buf.reset()
buf.add_str(text_line)
buf.guess_segment_properties()
hb.shape(hb_font, buf)
new_glyphs, end_glyph_pos = buf.get_glyphs(glyph_pos)
glyph_pos = end_glyph_pos
glyphs.extend(new_glyphs)
[g.index for g in glyphs]


# In[1]:


glyph_array = buf.get_glyphs_codepoint()
print(glyph_array)


# In[54]:


qah_face = qah.FontFace.create_for_ft_face(ft_face)
qah_face


# In[55]:


glyph_extents =     (qah.Context.create_for_dummy()
        .set_font_face(qah_face)
        .set_font_size(text_size)
        .glyph_extents(glyphs)
    )
figure_bounds = math.ceil(glyph_extents.bounds)
pix = qah.ImageSurface.create   (
    format = CAIRO.FORMAT_RGB24,
    dimensions = figure_bounds.dimensions
  )

# Actually render the glyphs into a Cairo context:


# In[56]:


(qah.Context.create(pix)
    .translate(- figure_bounds.topleft)
    .set_source_colour(Colour.grey(1))
    .paint()
    .set_source_colour(Colour.grey(0))
    .set_font_face(qah_face)
    .set_font_size(text_size)
    .show_glyphs(glyphs)
)


# In[57]:


pix.flush().write_to_png("b.png")

