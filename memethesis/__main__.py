from argparse import ArgumentParser
import sys
from .fancyprint import color
from .memethesizers import *
from .format_utils import *
from .meme.vertical import make_vertical
from .meme.horizontal import make_horizontal
from .meme.caption import make_caption
from .meme.imageops import stack
from .meme.separator import make_sep
from .interactive import interactive
from re import search, I

FORMATS = read_formats()
FMT_NAMES = get_format_names(FORMATS)
PANEL_TYPES = get_panel_types(FORMATS)


def main():
    argparser = ArgumentParser(description='All Your Memes Are Belong To Us!')

    ''' Frantic payload of arguments. '''
    argparser.add_argument(
        '-i', '--interactive', action='store_true',
        help='interactive mode'
    )
    argparser.add_argument(
        '-f', '--format', choices=FMT_NAMES,
        help=f'the meme format to use'
    )
    argparser.add_argument(
        '-o', '--output',
        help='the filename to save the meme as (default: ./meme.jpg)'
    )
    argparser.add_argument(
        '-p', '--preview', action='store_true',
        help='display the meme without saving it, unless -o/--output is specified'
    )

    argparser.add_argument(
        '-c', '--caption',
        help='caption text to add above your meme'
    )

    # parse flags from formats.yml
    for fk, fv in PANEL_TYPES.items():
        # fk: format names
        # fv.keys(): panel names
        # fv.values(): panel flags
        group = argparser.add_argument_group(fk)
        for pv in fv:
            group.add_argument('--' + str(pv))

    args = vars(argparser.parse_args())

    if args['interactive']:
        interactive()
    else:
        # non-interactive (pure-cli) mode
        # validate format
        if not args['format']:
            print(color(
                'Error: requires either -i/--interactive to be present or -f/--format specified.',
                fgc=1))  # red
            sys.exit(1)
        # make sure the meme to be generated has something else to be
        # other than an ephemeral spectre in the volatile RAM,
        # like a file or some screen pixels
        if not args['preview'] and not args['output']:
            print(color(
                'Error: either -p/--preview or -o/--output needs to be present.',
                fgc=1))
            sys.exit(1)

        fmt = args['format']

        # all the tuples with flags provided by formats.yml
        # are added to the list as (flag, value)
        # as a result, there are flags that are not populated.
        # to eliminate such "blank" tuples,
        # we run a filter against the list above.
        panels = list(filter(lambda tup: bool(tup[1]),
                        [(n, args[n.replace('-', '_')])
                         for n in PANEL_TYPES[fmt]]))
        # NOTE: argparse gives us --flag-with-dashes
        # as args['flag_with_dashes']

        if args['caption']:
            panels = [('caption', args['caption']), ('sep', None)] + panels

        meme = MEMETHESIZERS[fmt](fmt, panels)

        if args['preview']:
            # uses PIL to preview the meme with ImageMagick
            meme.show(title='Memethesis Preview')

        if args['output']:
            o = args['output']
            path = ((o if search('\.(jpe?g|png)$', o, flags=I) else o + '.jpg')
                    if o else 'meme.jpg')
            meme.save(path)
            print(color(f'Meme saved to {path}.', fgc=2))


if __name__ == '__main__':
    main()
