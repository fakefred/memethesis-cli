from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
from re import sub, split

WHITE = (255, 255, 255, 255)

# NYI
def is_CJK(char: str) -> bool:
    if len(char) == 1:
        point = ord(char)
        if (point in range(0x2E80, 0x9FFF)  # C, J
                or point in range(0xAC00, 0xD7FF)):  # K
            return True
    return False


def advanced_split(text: str) -> list:
    normal_split = split('\s+|\u200b+', text)
    further_split = []
    for piece in normal_split:
        for char in piece:
            if is_CJK(char):
                further_split.append(char)
            else:
                if len(further_split) == 0:
                    further_split.append(char)
                elif further_split[-1] == '' or not is_CJK(further_split[-1][-1]):
                    further_split[-1] += char
                else:
                    further_split.append(char)
        further_split.append('')
    # HACK remove all ''
    return list(filter(None, further_split))


def wrap_text(text: str, maxwidth: int, font) -> str:
    # maxwidth: in pixels
    # TODO: hyphenation

    # initiate drawing context
    canvas = Image.new('RGB', (1, 1), color=(255, 255, 255))
    draw = Draw(canvas)

    # split words and iterate
    words = advanced_split(text)
    current_line = ''
    wrapped_text = ''
    for word in words:
        line_width = draw.textsize(current_line + word, font=font)[0]
        if line_width <= maxwidth:
            # append word
            current_line += word + ' '
            wrapped_text += word + ' '
        else:
            # linebreak
            wrapped_text += '\n' + word + ' '
            # reset buffer
            current_line = word + ' '

    return wrapped_text


def make_text(text: str, box=(0, 0), font_path='', init_font_size=76,
              color=(0, 0, 0, 255), stroke=None,  # stroke can be a color tuple
              align='left', emojis={}, instance=''):
    ''' NYI
    if contains_emojis(text, emojis):
        # fancy rendering enabled
        # redirect to fit_text_with_emojis_in_box()
        return make_emoji_text(
            text, emojis=emojis, instance=instance,
            box=box, font_path=font_path, color=color,
            stroke=stroke, align=align)
    '''

    canvas = Image.new('RGBA', box, color=(255, 255, 255, 0))
    draw = Draw(canvas)
    textsize = (box[0] + 1, box[1] + 1)
    font_size = init_font_size  # max font size is 72; decrease by 4 until fit
    while textsize[0] > box[0] or textsize[1] > box[1]:  # doesn't fit
        if 0 < font_size <= 16:
            font_size -= 1
        elif 16 < font_size < 32:
            font_size -= 2
        elif font_size >= 32:
            font_size -= 4
        else:
            break
        font = truetype(font_path, size=font_size)
        # try to fit in the horizontal boundary
        wrapped = wrap_text(text, box[0], font)
        textsize = draw.multiline_textsize(wrapped, font=font)
        # when wrapped text fits in box, loop will exit, and font is remembered

    draw.multiline_text((0, 0), wrapped, fill=color if stroke is None else WHITE,
                        font=font, stroke_fill=stroke,
                        stroke_width=(max(font_size // 20, 2)
                                      if stroke is not None else 0), align=align)
    return canvas


# NYI
def make_emoji_text(text: str, emojis={}, instance='',
                    box=(0, 0), init_font_size=76, align='left',
                    font_path='', color=(0, 0, 0, 255), stroke=None):
    # different method
    # used for text with custom emojis
    # less efficient than without
    # TODO: flag for no-render-emoji
    # split text into individual words, then draw them sequentially.
    # NOTE: arg `align` is NYI, probably impossible
    words = advanced_split(text)
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

            emoji = get_emoji_if_is(
                word, size=font_size, instance=instance, emojis=emojis)
            # emoji: Image of it if is an emoji, else None
            word_width = (emoji.size[0]
                          if emoji
                          else draw.textsize(word, font=font)[0])

            # skip this size if even a single word won't fit
            if word_width > box[0]:
                break

            # fill line until it would overflow
            while x + word_width <= box[0]:
                if emoji:
                    if 'A' in emoji.getbands():
                        # emoji has Alpha channel, aka transparency
                        canvas.paste(emoji, box=(x, y), mask=emoji)
                    else:
                        canvas.paste(emoji, box=(x, y))
                else:
                    draw.text((x, y - font_size // 10),
                              word, fill=color if stroke is None else WHITE,
                              font=font, stroke_fill=stroke,
                              # stroke width: 2 is the bare minimum
                              stroke_width=(max(font_size // 20, 2)
                                            if stroke is not None else 0))

                x += word_width + (space_width if not is_CJK(word) else 0)

                idx += 1
                if idx >= len(words):
                    break

                word = words[idx]
                emoji = get_emoji_if_is(word, size=font_size,
                                        instance=instance, emojis=emojis)
                word_width = (emoji.size[0]
                              if emoji
                              else draw.textsize(words[idx], font=font)[0])

            y += line_height

        if y <= box[1] and idx == len(words):
            return canvas
