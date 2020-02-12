from .meme.vertical import make_vertical
from .meme.horizontal import make_horizontal
from .format_utils import *

MEMETHESIZERS_BY_FORMAT = {
    'vertical': make_vertical,
    'horizontal': make_horizontal
}
