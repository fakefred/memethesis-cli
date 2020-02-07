from PIL import Image, ImageDraw, ImageFont
from .caption import parse_caption, make_caption
from .separator import is_sep, make_sep
from .textops import make_text
from .imageops import stack
import re
from os import path

BLACK = (0, 0, 0, 255)
TRANSPARENT = (255, 255, 255, 0)

TEXTSPACE = (400, 250)

# TODO: automate memetheses, with only template image and text spaces provided in csv


def parse_drake(content: str):
    lines = content.splitlines()
    drakes = []  # tuples of (dislike/like, text)
    is_drake = False

    for line in lines:
        # remove zero-width spaces and leading/trailing whitespace
        naked_line = line.replace('\u200b', '').strip()
        # :drake_dislike: some text after it, not none [yes]
        # :drake_dislike: [no]
        if (naked_line.startswith(':drake_dislike: ') and
                naked_line.replace(':drake_dislike: ', '', 1).strip()):
            drakes.append((
                'dislike',
                # remove leftmost :drake_dislike:
                naked_line.replace(':drake_dislike: ', '', 1).strip()))
            is_drake = True

        elif (naked_line.startswith(':drake_like: ') and
                naked_line.replace(':drake_like: ', '', 1).strip()):
            drakes.append((
                'like',
                naked_line.replace(':drake_like: ', '', 1).strip()))
            is_drake = True

        elif parse_caption(naked_line) is not None:
            drakes.append((
                'caption',
                parse_caption(naked_line)
            ))

        elif is_sep(naked_line):
            drakes.append(('sep', ''))

    if is_drake:
        return drakes

    return None


def make_drake(drakes: list, emojis={},
               font=path.join(path.dirname(__file__),
                              'res/fonts/NotoSans-Regular.ttf'),
               instance='', saveto='drake_output.jpg', stroke=False):
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
                drake[1], emojis=emojis, box=TEXTSPACE, instance=instance,
                font_path=font, stroke=BLACK if stroke else None)
            temp.paste(text, box=(370, 12), mask=text)
            drake_panels.append(temp)

        elif drake[0] == 'like':
            temp = like_template.copy()
            text = make_text(
                drake[1], emojis=emojis, box=TEXTSPACE, instance=instance,
                font_path=font, stroke=BLACK if stroke else None)
            temp.paste(text, box=(370, 20), mask=text)
            drake_panels.append(temp)

        elif drake[0] == 'caption':
            drake_panels.append(
                make_caption(text=drake[1], emojis=emojis,
                             instance=instance, width=800, font=font,
                             stroke=stroke)
            )

        elif drake[0] == 'sep':
            drake_panels.append(make_sep(width=800))

    meme = stack(drake_panels)

    # meme.save(saveto)
    return meme
