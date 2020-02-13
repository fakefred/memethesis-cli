from PIL import Image
from .textops import make_text
from ..fonts import get_fontpath
import re


def make_caption(text='', width=800, height=120, margin=10, align='left',
                 font=get_fontpath('notosans'), stroke=None):
    caption = Image.new('RGBA', (width, height), color=(255, 255, 255, 255))
    cap_text = make_text(text, box=(width - 2 * margin, height - 2 * margin),
                         font_path=font, init_font_size=64,
                         align=align, stroke=stroke)
    caption.paste(cap_text, box=(10, 10), mask=cap_text)
    return caption
