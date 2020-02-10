from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
from re import sub, split

WHITE = (255, 255, 255, 255)


def make_text(text: str, box=(0, 0), init_font_size=76, align='left',
              font_path='', color=(0, 0, 0, 255), stroke=None):
    # split text into individual words, then draw them sequentially.
    # in fact more efficient than previously thought.
    # NOTE: arg `align` is NYI, probably impossible
    words = text.split()
    canvas = Image.new('RGBA', box, color=(255, 255, 255, 0))  # method scope

    x, y = 0, 0
    font_size = init_font_size

    while True:
        # (re-)initiate canvas
        canvas = Image.new('RGBA', box, color=(255, 255, 255, 0))
        draw = Draw(canvas)

        # for each font size, first fill the width.
        # if the height exceeds the size of the box, reduce font size.
        # repeat font size reduction until fits.
        if 0 < font_size <= 16:
            font_size -= 1
        elif 16 < font_size < 32:
            font_size -= 2
        elif font_size >= 32:
            font_size -= 4
        else:
            break

        font = truetype(font_path, size=font_size)
        space_width = draw.textsize(' ', font=font)[0]
        line_height = int(font_size * 1.2)

        # start filling words
        idx = 0  # position in list `words`
        y = 0
        while idx < len(words):  # words not depleted
            # new line
            x = 0
            word = words[idx]

            word_width = draw.textsize(word, font=font)[0]

            # skip this size if even a single word won't fit
            if word_width > box[0]:
                break

            # fill line until it would overflow
            while x + word_width <= box[0]:
                draw.text((x, y - font_size // 10),
                          word, fill=color if stroke is None else WHITE,
                          font=font, stroke_fill=stroke,
                          # stroke width: 2 is the bare minimum
                          stroke_width=(max(font_size // 20, 2)
                                        if stroke is not None else 0))

                x += word_width + space_width

                idx += 1
                if idx >= len(words):
                    break

                word = words[idx]
                word_width = draw.textsize(words[idx], font=font)[0]

            y += line_height

        if y <= box[1] and idx == len(words):
            return canvas
