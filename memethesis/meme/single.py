from PIL import Image, ImageDraw, ImageFont
import yaml
from ..fancyprint import color
from .caption import make_caption
from .separator import make_sep
from .textops import make_text
from .imageops import stack
from ..format_utils import read_formats
from os import path
import sys

FORMATS = read_formats()

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)


def make_single(format: str, entities: list,
                font=path.join(path.dirname(__file__),
                               'res/fonts/NotoSans-Regular.ttf')):
    format_info = FORMATS[format]
    if not format_info['composition'] == 'single':
        print(color(
            f'Error: meme format `{format}` is not single-panel.',
            fgc=1))
        sys.exit(1)

    panel = format_info['panels']
    template = Image.open(
        path.join(path.dirname(__file__), 'res/template', format_info['image']))

    for ent in entities:
        if ent[0] in panel.keys():
            box = panel[ent[0]]['textbox']
            style = (panel[ent[0]]['style']
                     if 'style' in panel[ent[0]] else None)
            text = make_text(
                ent[1], box=box[2:], font_path=font,
                stroke=BLACK if style == 'stroke' else None)
            template.paste(text, box=box[:2], mask=text)

    return template
