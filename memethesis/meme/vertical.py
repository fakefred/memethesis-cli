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


def make_vertical(format: str, entities: list,
                  font=path.join(path.dirname(__file__),
                                 'res/fonts/NotoSans-Regular.ttf'),
                  saveto='generic_vertical_output.jpg', stroke=False):
    format_info = FORMATS[format]
    if not format_info['composition'] == 'vertical':
        print(color(
            f'Error: meme format `{format}` is not vertically stacked.',
            fgc=1))
        sys.exit(1)

    panels = format_info['panels']
    templates = {k: Image.open(
        path.join(path.dirname(__file__), "res/template", v["image"])
    ) for k, v in panels.items()}
    textboxes = {k: v['textbox'] for k, v in panels.items()}
    # textboxes[i] = [left top width height]

    generated_panels = []

    for ent in entities:
        # ent = (identifier, text) or its list equivalent
        if ent[0] in panels.keys():
            # Image.paste() overwrites Image
            temp = templates[ent[0]].copy()
            text = make_text(
                ent[1], box=textboxes[ent[0]][2:], font_path=font,
                stroke=BLACK if stroke else None)
            temp.paste(text, box=textboxes[ent[0]][:2], mask=text)
            generated_panels.append(temp)

        elif ent[0] == 'caption':
            generated_panels.append(
                make_caption(text=ent[1], font=font, stroke=stroke,
                             width=list(templates.values())[0].size[0]))
            # assumes constant widths

        elif ent[0] == 'sep':
            generated_panels.append(
                make_sep(width=list(templates.values())[0].size[0]))

    meme = stack(generated_panels)
    return meme
