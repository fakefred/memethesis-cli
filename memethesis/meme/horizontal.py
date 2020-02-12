from PIL import Image, ImageDraw, ImageFont
import yaml
from ..fancyprint import color
from .caption import make_caption
from .separator import make_sep
from .textops import make_text
from .imageops import stack, lay
from ..format_utils import read_formats
from os import path
import sys

FORMATS = read_formats()

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)


def make_horizontal(format, entities: list,
                    font=path.join(path.dirname(__file__),
                                   'res/fonts/NotoSans-Regular.ttf'),
                    saveto='horizontal_output.jpg', stroke=False):
    format_info = FORMATS[format]
    if not format_info['composition'] == 'horizontal':
        print(color(
            f'Error: meme format `{format}` is not horizontally laid.',
            fgc=1))
        sys.exit(1)

    panels = format_info['panels']
    templates = {k: Image.open(
        path.join(path.dirname(__file__), "res/template", v["image"])
    ) for k, v in panels.items()}
    textboxes = {k: v['textbox'] for k, v in panels.items()}

    body_panels = []

    for ent in entities:
        if ent[0] in panels.keys():
            temp = templates[ent[0]].copy()
            text = make_text(
                ent[1], box=textboxes[ent[0]][2:], font_path=font,
                stroke=BLACK if stroke else None)
            temp.paste(text, box=textboxes[ent[0]][:2], mask=text)
            body_panels.append(temp)

    body = lay(body_panels)
    meme_width = body.size[0]

    # until now the meme width had been unknown
    # now we can make caps and seps
    cap_seps = []
    for ent in entities:
        if ent[0] == 'caption':
            cap_seps.append(
                make_caption(text=ent[1], width=meme_width,
                             font=font, stroke=stroke)
            )
        elif ent[0] == 'sep':
            cap_seps.append(make_sep(width=meme_width))

    meme = stack(cap_seps + [body])
    return meme
