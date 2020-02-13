from PIL import Image, ImageDraw
import yaml
from ..fancyprint import color
from .caption import make_caption
from .separator import make_sep
from .textops import make_text
from ..fonts import get_fontpath
from .imageops import stack, lay
from ..format_utils import read_formats
from os import path
import sys

FORMATS = read_formats()

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)


def make_horizontal(format, entities: list):
    format_info = FORMATS[format]
    if not format_info['composition'] == 'horizontal':
        print(color(
            f'Error: meme format `{format}` is not horizontally laid.',
            fgc=1))
        sys.exit(1)

    panels = format_info['panels']

    global_font = get_fontpath(
        format_info['font'] if 'font' in format_info
        else 'notosans')
    global_style = format_info['style'] if 'style' in format_info else None

    body_panels = []

    for name, text in entities:
        if name in panels.keys():
            meta = panels[name]
            style = (meta['style']
                     if 'style' in meta else global_style)
            font = (get_fontpath(meta['font'])
                    if 'font' in meta else global_font)

            temp = Image.open(path.join(
                path.dirname(__file__),
                'res/template', meta['image']))

            text = make_text(
                text, box=meta['textbox'][2:], font_path=font,
                stroke=BLACK if style == 'stroke' else None)
            temp.paste(text, box=meta['textbox'][:2], mask=text)
            body_panels.append(temp)

    body = lay(body_panels)
    meme_width = body.size[0]

    # until now the meme width had been unknown
    # now we can make caps and seps
    cap_seps = []
    for name, text in entities:
        if name == 'caption':
            cap_seps.append(
                make_caption(text=text, width=meme_width, font=global_font,
                             stroke=BLACK if global_style == 'stroke' else None)
            )
        elif name == 'sep':
            cap_seps.append(make_sep(width=meme_width))

    meme = stack(cap_seps + [body])
    return meme
