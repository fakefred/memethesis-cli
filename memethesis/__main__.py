from argparse import ArgumentParser
import sys
import re
from os import path
from .fancyprint import color, style
from .memethesizers import *
from .format_utils import *
from .interactive import interactive

FORMATS = read_formats()
FMT_NAMES = get_format_names(FORMATS)
PANEL_TYPES = get_panel_types(FORMATS)


def main():
    argparser = ArgumentParser(add_help=False)

    argparser.add_argument(
        '-h', '--help', action='store_true')
    argparser.add_argument(
        '-l', '--list', action='store_true')
    argparser.add_argument(
        '-i', '--interactive', action='store_true')
    argparser.add_argument(
        '-f', '--format', choices=FMT_NAMES)
    argparser.add_argument(
        '-o', '--output')
    argparser.add_argument(
        '-p', '--preview', action='store_true')
    argparser.add_argument(
        '-c', '--caption')

    # parse flags from formats.yml
    for fk, fv in PANEL_TYPES.items():
        # fk: format names
        # fv.keys(): panel names
        # fv.values(): panel flags
        group = argparser.add_argument_group(fk)
        for pv in fv:
            group.add_argument('--' + str(pv))

    args = vars(argparser.parse_args())

    if args['help']:
        print(''.join(
            open(
                path.join(path.dirname(__file__), 'help.txt')
            ).readlines()))
        sys.exit(0)
    elif args['list']:
        # format:
        #   flag[: description]
        ls = ''
        for fmt in FMT_NAMES:
            ls += style(fmt, sty=1) + '\n'
            types = PANEL_TYPES[fmt]
            for ty in types:
                meta = FORMATS[fmt]['panels'][ty]
                ls += '  --' + ty
                if 'description' in meta and meta['description']:
                    ls += ': ' + meta['description']
                ls += '\n'
        print(ls)
        sys.exit(0)

    elif args['interactive']:
        interactive()
    else:
        # command mode
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
            fp = ((o if re.search('\.(jpe?g|png)$', o, flags=re.I)
                   else o + '.jpg')
                  if o else 'meme.jpg')
            meme.save(fp)
            print(color(f'Meme saved to {fp}.', fgc=2))


if __name__ == '__main__':
    main()
