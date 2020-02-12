from .meme.vertical import make_vertical
from .meme.horizontal import make_horizontal
from .meme.single import make_single
from .format_utils import *

MEMETHESIZERS_BY_FORMAT = {
    'vertical': make_vertical,
    'horizontal': make_horizontal,
    'single': make_single
}
