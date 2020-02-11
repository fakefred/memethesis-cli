from PIL import Image, ImageDraw, ImageFont
from .caption import make_caption
from .separator import make_sep
from .textops import make_text
from .imageops import stack
import re
from os import path

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACE = (400, 250)


def make_drake(drakes: list,
               font=path.join(path.dirname(__file__),
                              'res/fonts/NotoSans-Regular.ttf'),
               saveto='drake_output.jpg', stroke=False):
    dislike_template = Image.open(
        path.join(path.dirname(__file__), 'res/template/drake/drake_dislike.jpg'))
    like_template = Image.open(
        path.join(path.dirname(__file__), 'res/template/drake/drake_like.jpg'))

    drake_panels = []

    for drake in drakes:
        # drake = ('dislike'/'like', text)
        if drake[0] == 'dislike':
            # Image.paste() overwrites Image
            temp = dislike_template.copy()
            text = make_text(
                drake[1], box=TEXTSPACE, font_path=font,
                stroke=BLACK if stroke else None)
            temp.paste(text, box=(370, 12), mask=text)
            drake_panels.append(temp)

        elif drake[0] == 'like':
            temp = like_template.copy()
            text = make_text(
                drake[1], box=TEXTSPACE, font_path=font,
                stroke=BLACK if stroke else None)
            temp.paste(text, box=(370, 20), mask=text)
            drake_panels.append(temp)

        elif drake[0] == 'caption':
            drake_panels.append(
                make_caption(text=drake[1], width=800,
                             font=font, stroke=stroke))

        elif drake[0] == 'sep':
            drake_panels.append(make_sep(width=800))

    meme = stack(drake_panels)

    # meme.save(saveto)
    return meme
