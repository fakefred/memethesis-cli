from argparse import ArgumentParser
import sys
from .fancyprint import color
from .meme.vertical import make_vertical
from .meme.woman_yelling import make_woman_yelling
from .meme.caption import make_caption
from .meme.imageops import stack
from .meme.separator import make_sep
from .interactive import interactive
from re import search, I

FORMATS = ['drake', 'brainsize', 'womanyelling', 'pooh']


def main():
    argparser = ArgumentParser(description='All Your Memes Are Belong To Us!')

    ''' Frantic payload of arguments. '''
    argparser.add_argument(
        '-i', '--interactive', action='store_true',
        help='interactive mode'
    )
    argparser.add_argument(
        '-f', '--format', choices=FORMATS,
        help=f'the meme format to use (Supported: {", ".join(FORMATS)})'
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

    drake_args = argparser.add_argument_group('Drake')
    drake_args.add_argument('--dislike', required=False)
    drake_args.add_argument('--like', required=False)

    brainsize_args = argparser.add_argument_group('Brain Size')
    for i in range(1, 15):
        brainsize_args.add_argument(
            '-s{}'.format(i), '--size{}'.format(i), required=False
        )

    womanyelling_args = argparser.add_argument_group('Woman Yelling')
    womanyelling_args.add_argument('--woman', required=False)
    womanyelling_args.add_argument('--cat', required=False)

    pooh_args = argparser.add_argument_group('Winnie the Pooh')
    pooh_args.add_argument('--tired', required=False)
    pooh_args.add_argument('--wired', required=False)

    args = argparser.parse_args()

    if args.interactive:
        interactive()
    else:
        # non-interactive (pure-cli) mode

        # validate format
        if not args.format:
            print(color(
                'Error: requires either -i/--interactive to be present or -f/--format specified.',
                fgc=1))  # red
            sys.exit(1)
        # make sure the meme to be generated has something else to be
        # other than an ephemeral spectre in the volatile RAM,
        # like a file or some screen pixels
        if not args.preview and not args.output:
            print(color(
                'Error: either -p/--preview or -o/--output needs to be present.',
                fgc=1))
            sys.exit(1)

        if args.format == 'drake':
            if args.dislike and args.like:
                meme = make_vertical('drake', [
                    ('dislike', args.dislike),
                    ('like', args.like)
                ])
            else:
                print(color(
                    'Error: Drake memes require both --dislike and --like.',
                    fgc=1))
                sys.exit(1)  # show user an error right in their face

        elif args.format == 'brainsize':
            brain_args=[args.size1, args.size2, args.size3, args.size4,
                          args.size5, args.size6, args.size7,
                          args.size8, args.size9, args.size10, args.size11,
                          args.size12, args.size13, args.size14]  # lifehack!
            if any(brain_args):
                brains=[]
                for size, text in enumerate(brain_args, start=1):
                    if text is not None:
                        brains.append((size, text))
                meme=make_vertical('brainsize', brains)
            else:
                print(color(
                    'Error: Brain Size memes require at least one brain size',
                    fgc=1))
                sys.exit(1)
        elif args.format == 'womanyelling':
            if args.woman and args.cat:
                meme=make_woman_yelling('', [
                    ('woman', args.woman),
                    ('cat', args.cat)
                ])
            else:
                print(color(
                    'Error: Woman Yelling memes require both --woman and --cat.',
                    fgc=1))
                sys.exit(1)
        elif args.format == 'pooh':
            if args.tired and args.wired:
                meme=make_vertical('pooh', [
                    ('tired', args.tired),
                    ('wired', args.wired)
                ])
            else:
                print(color(
                    'Error: Pooh memes requires both --tired and --wired.',
                    fgc=1))
                sys.exit(1)

        if args.caption:
            meme=stack([
                make_caption(text=args.caption, width=meme.size[0]),
                make_sep(width=meme.size[0]),
                meme
            ])

        if args.preview:
            # uses PIL to preview the meme with ImageMagick
            meme.show(title='Memethesis Preview')

        if args.output:
            o=args.output
            path=((o if search('\.(jpe?g|png)$', o, flags=I) else o + '.jpg')
                    if o else 'meme.jpg')
            meme.save(path)
            print(color(f'Meme saved to {path}.', fgc=2))


if __name__ == '__main__':
    main()
