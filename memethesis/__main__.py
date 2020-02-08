from argparse import ArgumentParser
import sys
from PyInquirer import prompt
from .meme.drake import make_drake
from .meme.brainsize import make_brainsize
from .meme.woman_yelling import make_woman_yelling
from .meme.caption import make_caption
from .meme.imageops import stack
from .meme.separator import make_sep
from .interactive import interactive

FORMATS = ['drake', 'brainsize', 'womanyelling']


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

    brainsize_args = argparser.add_argument_group(
        'Brain Size (so many sizes thanks to Brian)')
    for i in range(1, 15):
        brainsize_args.add_argument(
            '-s{}'.format(i), '--size{}'.format(i), required=False
        )

    womanyelling_args = argparser.add_argument_group('Woman Yelling')
    womanyelling_args.add_argument('--woman', required=False)
    womanyelling_args.add_argument('--cat', required=False)

    args = argparser.parse_args()

    if args.interactive:
        interactive()
    else:
        # non-interactive (pure-cli) mode

        # validate format
        if not args.format:
            print('Error: -f/--format needs to be specified.')
            sys.exit(1)
        # make sure the meme to be generated has something else to be
        # other than an ephemeral spectre in the volatile RAM,
        # like a file or some screen pixels
        if not args.preview and not args.output:
            print('Error: either -p/--preview or -o/--output needs to be present.')
            sys.exit(1)

        if args.format == 'drake':
            if args.dislike and args.like:
                meme = make_drake([
                    ('dislike', args.dislike),
                    ('like', args.like)
                ])
            else:
                print('Error: Drake memes require both --dislike and --like.')
                sys.exit(1)  # show user an error right in their face

        elif args.format == 'brainsize':
            brain_args = [args.size1, args.size2, args.size3, args.size4,
                          args.size5, args.size6, args.size7,
                          args.size8, args.size9, args.size10, args.size11,
                          args.size12, args.size13, args.size14]  # lifehack!
            if any(brain_args):
                brains = []
                for size, text in enumerate(brain_args, start=1):
                    if text is not None:
                        brains.append((size, text))
                meme = make_brainsize(brains)
            else:
                print('Error: Brain Size memes require at least one brain size')
                sys.exit(1)
        elif args.format == 'womanyelling':
            if args.woman and args.cat:
                meme = make_woman_yelling([
                    ('woman', args.woman),
                    ('cat', args.cat)
                ])
            else:
                print('Error: Woman Yelling memes require both --woman and --cat.')
                sys.exit(1)

        if args.caption:
            meme = stack([
                make_caption(text=args.caption),
                make_sep(width=meme.size[0]),
                meme
            ])

        if args.preview:
            # uses PIL to preview the meme with ImageMagick
            meme.show(title='Memethesis Preview')

        if args.output:
            o = args.output
            meme.save((o if o.endswith('.jpg') else o + '.jpg')
                      if o else 'meme.jpg')


if __name__ == '__main__':
    main()
