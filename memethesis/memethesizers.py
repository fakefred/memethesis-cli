from .meme.vertical import make_vertical
from .meme.horizontal import make_horizontal
from .meme.single import make_single
from .format_utils import *

FORMATS = read_formats()
COMPOSITORS = {
    'vertical': make_vertical,
    'horizontal': make_horizontal,
    'single': make_single
}
MEMETHESIZERS = {k: COMPOSITORS[v]
                 for k, v in get_compositions(FORMATS).items()}
