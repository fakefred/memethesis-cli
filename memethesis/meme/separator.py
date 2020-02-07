from PIL import Image


def is_sep(line: str) -> bool:
    # line consists of >=3 dashes
    return len(line.strip()) >= 3 and all([char == '-' for char in line.strip()])


def make_sep(width=800):
    return Image.new('RGBA', (width, 3), color=(0, 0, 0, 255))
