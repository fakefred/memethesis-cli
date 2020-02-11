from PIL import Image, ImageDraw, ImageFont
from .caption import make_caption
from .separator import make_sep
from .textops import make_text
from .imageops import stack, lay
import re
from os import path

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACE = (480, 160)


def make_woman_yelling(format, entities: list,  # format is a dummy arg
                       font=path.join(path.dirname(__file__),
                                      'res/fonts/NotoSans-Regular.ttf'),
                       saveto='woman_yelling_output.jpg', stroke=False):
    '''
    Procedure:
    1. for each body panel (woman/cat), stack its text and image, and
       append to body_panels
    2. lay (horizontally) panels in body_panels
    3. stack up all captions and seps and finally the image laid in step 2
    '''
    woman_template = Image.open(
        path.join(path.dirname(__file__),
                  'res/template/woman_yelling/taylor.jpg'))
    cat_template = Image.open(
        path.join(path.dirname(__file__),
                  'res/template/woman_yelling/catto.jpg'))

    body_panels = []

    for entity in entities:
        # entity = ('woman'/'cat', text)
        if entity[0] == 'woman':
            body_panels.append(stack([
                make_caption(text=entity[1],
                             width=woman_template.size[0], height=TEXTSPACE[1],
                             font=font, align='center', margin=20,
                             stroke=stroke),
                # the align='center' is disregarded by make_emoji_text
                woman_template
            ]))

        elif entity[0] == 'cat':
            body_panels.append(stack([
                make_caption(text=entity[1],
                             width=cat_template.size[0], height=TEXTSPACE[1],
                             font=font, align='center', margin=20,
                             stroke=stroke),
                cat_template
            ]))

    body = lay(body_panels)
    meme_width = body.size[0]

    # until now the meme width had been unknown
    # now we can make caps and seps
    cap_seps = []
    for entity in entities:
        if entity[0] == 'caption':
            cap_seps.append(
                make_caption(text=entity[1], width=meme_width,
                             font=font, stroke=stroke)
            )
        elif entity[0] == 'sep':
            cap_seps.append(make_sep(width=meme_width))

    meme = stack(cap_seps + [body])

    # meme.save(saveto)
    return meme
