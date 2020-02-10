from PIL import Image, ImageDraw, ImageFont
from .caption import make_caption
from .separator import make_sep
from .textops import make_text
from .imageops import stack
from os import path

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACE = (300, 240)


def make_pooh(poohs: list,
              font=path.join(path.dirname(__file__),
                             'res/fonts/NotoSans-Regular.ttf'),
              saveto='pooh_output.jpg', stroke=False):
    tired_template = Image.open(
        path.join(path.dirname(__file__), 'res/template/pooh/tired.jpg'))
    wired_template = Image.open(
        path.join(path.dirname(__file__), 'res/template/pooh/wired.jpg'))

    pooh_panels = []

    for pooh in poohs:
        if pooh[0] == 'tired':
            temp = tired_template.copy()
            text = make_text(
                pooh[1],  box=TEXTSPACE, font_path=font,
                stroke=BLACK if stroke else None)
            temp.paste(text, box=(370, 10), mask=text)
            pooh_panels.append(temp)

        elif pooh[0] == 'wired':
            temp = wired_template.copy()
            text = make_text(
                pooh[1],  box=TEXTSPACE, font_path=font,
                stroke=BLACK if stroke else None)
            temp.paste(text, box=(370, 10), mask=text)
            pooh_panels.append(temp)

        elif pooh[0] == 'caption':
            pooh_panels.append(
                make_caption(text=pooh[1], width=680,
                             font=font, stroke=stroke))

        elif pooh[0] == 'sep':
            pooh_panels.append(make_sep(width=680))

    meme = stack(pooh_panels)

    return meme
