from PIL import Image
from .textops import make_text
import re


def make_caption(text='', width=800, height=120, margin=10, align='left',
                 font='./res/fonts/NotoSans-Regular.ttf', stroke=False):
    caption = Image.new('RGBA', (width, height), color=(255, 255, 255, 255))
    cap_text = make_text(text, box=(width - 2 * margin, height - 2 * margin),
                         font_path=font, init_font_size=64,
                         align=align, stroke=(0, 0, 0, 255) if stroke else None)
    caption.paste(cap_text, box=(10, 10), mask=cap_text)
    return caption
