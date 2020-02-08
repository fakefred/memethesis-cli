from PIL import Image, ImageDraw, ImageFont
from .caption import parse_caption, make_caption
from .separator import is_sep, make_sep
from .textops import make_text
from .imageops import stack, lay
import re
from os import path

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACE = (480, 160)

WOMAN = ':women_yelling: '  # this is the de facto emoji shortcode on m.t
CAT = ':catto: '


def parse_woman_yelling(content: str):
    lines = content.splitlines()
    entities = []  # tuples of (woman/cat, text)
    is_woman_yelling = False

    for line in lines:
        # remove zero-width spaces and leading/trailing whitespace
        naked_line = line.replace('\u200b', '').strip()
        if (naked_line.startswith(WOMAN) and
                naked_line.replace(WOMAN, '', 1).strip()):
            entities.append((
                'woman',
                naked_line.replace(WOMAN, '', 1).strip()))
            is_woman_yelling = True

        elif (naked_line.startswith(CAT) and
                naked_line.replace(CAT, '', 1).strip()):
            entities.append((
                'cat',
                naked_line.replace(CAT, '', 1).strip()))
            is_woman_yelling = True

        elif not is_woman_yelling and parse_caption(naked_line) is not None:
            # only allow captions and seps above woman and cat
            entities.append((
                'caption',
                parse_caption(naked_line)
            ))

        elif not is_woman_yelling and is_sep(naked_line):
            entities.append(('sep', ''))

    if is_woman_yelling:
        return entities

    return None


def make_woman_yelling(entities: list, emojis={},
                       font=path.join(path.dirname(__file__),
                                      'res/fonts/NotoSans-Regular.ttf'),
                       instance='', saveto='woman_yelling_output.jpg', stroke=False):
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
                make_caption(text=entity[1], emojis=emojis, instance=instance,
                             width=woman_template.size[0], height=TEXTSPACE[1],
                             font=font, align='center', margin=20,
                             stroke=stroke),
                # the align='center' is disregarded by make_emoji_text
                woman_template
            ]))

        elif entity[0] == 'cat':
            body_panels.append(stack([
                make_caption(text=entity[1], emojis=emojis, instance=instance,
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
                make_caption(text=entity[1], emojis=emojis,
                             instance=instance, width=meme_width, font=font,
                             stroke=stroke)
            )
        elif entity[0] == 'sep':
            cap_seps.append(make_sep(width=meme_width))

    meme = stack(cap_seps + [body])

    # meme.save(saveto)
    return meme
