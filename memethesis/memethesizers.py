from .meme.vertical import make_vertical
from .meme.woman_yelling import make_woman_yelling
from .format_utils import *


MEMETHESIZERS_BY_FORMAT = {
    'vertical': make_vertical,
    'woman_yelling': make_woman_yelling
}