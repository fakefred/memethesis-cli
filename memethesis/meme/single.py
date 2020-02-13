from PIL import Image, ImageDraw
import yaml
from ..fancyprint import color
from .caption import make_caption
from .separator import make_sep
from .textops import make_text
from ..fonts import get_fontpath
from .imageops import stack
from ..format_utils import read_formats
from os import path
import sys

FORMATS = read_formats()

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)


def make_single(format: str, entities: list):
    format_info = FORMATS[format]
    if not format_info['composition'] == 'single':
        print(color(
            f'Error: meme format `{format}` is not single-panel.',
            fgc=1))
        sys.exit(1)

    panel = format_info['panels']
    template = Image.open(
        path.join(path.dirname(__file__), 'res/template', format_info['image']))

    global_font = get_fontpath(
        format_info['font'] if 'font' in format_info
        else 'notosans')
    global_style = format_info['style'] if 'style' in format_info else None

    layers = []

    for name, text in entities:
        if name in panel.keys():
            meta = panel[name]
            position = meta['textbox']

            font = (get_fontpath(meta['font'])
                    if 'font' in meta else global_font)
            style = (meta['style']
                     if 'style' in meta else global_style)

            text = make_text(
                text, box=position[2:], font_path=font,
                stroke=BLACK if style == 'stroke' else None)
            # NOTE: this procedure is unreusable
            # because `template` is overwritten
            template.paste(text, box=position[:2], mask=text)

        elif name == 'caption':
            layers.append(
                make_caption(text=text, width=template.size[0], font=global_font,
                             stroke=BLACK if global_style == 'stroke' else None))

        elif name == 'sep':
            layers.append(
                make_sep(width=template.size[0]))

    return stack(layers + [template])
