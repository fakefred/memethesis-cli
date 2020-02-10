from PIL import Image, ImageDraw, ImageFont
from .caption import make_caption
from .separator import make_sep
from .textops import make_text
from .imageops import stack
from re import match
from os import path

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACES = [(380, 250),  # these brain size
              (380, 250),  # panels have
              (380, 240),  # various heights
              (380, 255),
              (380, 250),
              (380, 280),  # 14
              (380, 270),  # fucking
              (380, 280),  # brain
              (380, 250),  # sizes
              (380, 260),  # thanks
              (380, 290),  # to
              (380, 280),  # brian
              (380, 240),
              (380, 400)]


def make_brainsize(brains: list,
                   font=path.join(path.dirname(__file__),
                                  'res/fonts/NotoSans-Regular.ttf'),
                   saveto='brain_output.jpg', stroke=False):
    templates = [Image.open(
        path.join(
            path.dirname(__file__),
            f'res/template/brainsize/brain{n}.jpg'
        )) for n in range(1, 15)]
    # templates[n] = meme template panel for brain size n+1

    brain_panels = []

    for brain in brains:
        # brain = ([1-14], text)
        if brain[0] in range(1, 15):
            temp = templates[brain[0] - 1].copy()
            text = make_text(
                brain[1], box=TEXTSPACES[brain[0] - 1],
                font_path=font, stroke=BLACK if stroke else None)
            temp.paste(text, box=(10, 8), mask=text)
            brain_panels.append(temp)
        elif brain[0] == 'caption':
            brain_panels.append(
                make_caption(text=brain[1], width=800,
                             font=font, stroke=stroke)
            )
        elif brain[0] == 'sep':
            brain_panels.append(make_sep(width=800))

    meme = stack(brain_panels)

    # meme.save(saveto)
    return meme
