import sys
from PyInquirer import prompt
from .colorprint import color
from .meme.drake import make_drake
from .meme.brainsize import make_brainsize
from .meme.woman_yelling import make_woman_yelling
from .meme.caption import make_caption
from .meme.imageops import stack
from .meme.separator import make_sep

FORMATS = ['drake', 'brainsize', 'womanyelling']

PANEL_TYPES = {
    'drake': ['dislike', 'like'],
    # 'brainsize': [i for i in range(1, 15)],
    'brainsize': list(range(1, 15)),
    'womanyelling': ['woman', 'cat']
}

DISP_TYPES = {
    'dislike': 'Drake dislike',
    'like': 'Drake like',
    **dict([(sz, 'Brain size ' + str(sz)) for sz in range(1, 15)]),
    'woman': 'Woman yelling',
    'cat': 'Confused cat',
    'caption': 'Caption',
    'sep': 'Horizontal line',
    'abort': '[abort: stop adding panels]'
}

DISP_TYPES_REVERSE = {v: k for k, v in DISP_TYPES.items()}

MEMETHESIZERS = {
    'drake': make_drake,
    'brainsize': make_brainsize,
    'womanyelling': make_woman_yelling
}


def panel_memory(panels: list) -> str:
    output = 'Current panels:\n'
    for i, p in enumerate(panels, 1):
        output += f'{i}. {DISP_TYPES[p[0]]}: {p[1]}\n'
    return output


def interactive():
    # ask for format
    format = prompt([{
        'type': 'list',
        'name': 'format',
        'message': 'Select meme format:',
        'choices': FORMATS
    }])['format']

    panel_types_of_format = PANEL_TYPES[format]

    panels = []
    # cap and sep are rejected after woman/cat panel.
    reject_cap_and_sep = False
    loop = True
    # begin adding panels
    while loop:
        applicable_panel_types = (panel_types_of_format +
                                  (['caption', 'sep']
                                   if not reject_cap_and_sep else []) +
                                  ['abort'])
        displayed_panel_types = [DISP_TYPES[k]
                                 for k in applicable_panel_types]

        # ask for panel type
        panel_type = DISP_TYPES_REVERSE[prompt([{
            'type': 'list',
            'name': 'type',
            'message': f'Select type for panel {len(panels) + 1}:',
            'choices': displayed_panel_types
        }])['type']]

        if panel_type == 'abort':
            break  # exit loop, proceed to panel editing

        if not panel_type == 'sep':
            # sep lines do not need text
            text = prompt([{
                'type': 'input',
                'name': 'text',
                'message': f'Text for panel {len(panels) + 1}: (leave blank to abort)',
            }])['text']
            if not text:
                continue  # return to panel type selection
        else:
            text = ''

        if panel_type in ('woman', 'cat') and not reject_cap_and_sep:
            # notify at first woman/cat panel addition
            print(color('Warning: after the addition of a woman or cat panel, \
captions and lines are no longer accepted.', fgc=3))  # yellow
            reject_cap_and_sep = True

        panels.append([panel_type, text])
        print(panel_memory(panels))

        loop = prompt([{
            'type': 'confirm',
            'name': 'loop',
            'message': 'Add another panel?',
            'default': True
        }])['loop']

        if not loop and all([(p[0] in ('caption', 'sep')) for p in panels]):
            # no body panels added
            print(color(
                'Error: cannot proceed until a real meme panel is added.',
                fgc=1))  # red
            loop = True

    # begin editing panels
    loop = True
    while loop:
        print('This is a list of panels you have added to your meme:')
        print(panel_memory(panels))
        preview = prompt([{
            'type': 'confirm',
            'name': 'preview',
            'message': 'Display a preview of your meme?',
            'default': True
        }])['preview']
        if preview:
            MEMETHESIZERS[format](panels).show()

        loop = prompt([{
            'type': 'confirm',
            'name': 'modify',
            'message': 'Any further modifications to make?',
            'default': False
        }])['modify']

        if loop:  # modify
            num = prompt([{
                'type': 'input',
                'name': 'num',
                'message': 'Enter panel # to edit / remove / insert another panel after:',
                'validate': lambda s: (s.isdecimal() and
                                       (0 < int(s) < len(panels) + 1)),
                'filter': lambda s: int(s)
            }])['num']

            prop = prompt([{
                'type': 'list',
                'name': 'prop',
                'message': 'Select how the panel should be modified:',
                'choices': ((['Edit text', 'Edit type']
                             if panels[num - 1][0] not in ('line', 'sep') else []) +
                            ['Insert after', 'Remove'])
            }])['prop']

            if prop == 'Edit text':
                panels[num - 1][1] = prompt([{
                    'type': 'input',
                    'name': 'text',
                    'message': f'Text for panel {num}:',
                    'default': panels[num - 1][1],
                    'validate': lambda s: bool(s)
                }])['text']
            elif prop == 'Edit type':
                panels[num - 1][0] = DISP_TYPES_REVERSE[prompt([{
                    'type': 'list',
                    'name': 'type',
                    'message': f'Select type for panel:',
                    'choices': displayed_panel_types
                    # NOTE: for womanyelling, cap and sep stay rejected
                }])['type']]
            elif prop == 'Insert after':
                applicable_panel_types = (panel_types_of_format +
                                          (['caption', 'sep']
                                           if not reject_cap_and_sep else []) +
                                          ['abort'])
                displayed_panel_types = [DISP_TYPES[k]
                                         for k in applicable_panel_types]
                new_panel_confirmed = False
                while not new_panel_confirmed:
                    # ask for panel type
                    panel_type = DISP_TYPES_REVERSE[prompt([{
                        'type': 'list',
                        'name': 'type',
                        'message': f'Select type for panel {len(panels) + 1}:',
                        'choices': displayed_panel_types
                    }])['type']]

                    if panel_type == 'abort':
                        break  # exit loop, proceed to panel editing

                    if not panel_type == 'sep':
                        # sep lines do not need text
                        text = prompt([{
                            'type': 'input',
                            'name': 'text',
                            'message': f'Text for panel {len(panels) + 1}: (leave blank to abort)',
                        }])['text']
                        if not text:
                            # return to 'print current panels /
                            # ask if preview is needed' part
                            continue
                    else:
                        text = ''

                    panels = panels[:num] + [[panel_type, text]] + panels[num:]
                    print(panel_memory(panels))
                    new_panel_confirmed = True

            elif prop == 'Remove':
                # connect two splices of `panels` before and after (num - 1)
                panels = panels[:(num - 1)] + panels[num:]

    # all panels recorded
    # begin memethesizing
    o = prompt([{
        'type': 'input',
        'name': 'saveto',
        'message': f'Save meme to: (only .jpg supported)',
        'validate': lambda s: bool(s)
    }])['saveto']

    MEMETHESIZERS[format](panels).save((o if o.endswith('.jpg') else o + '.jpg')
              if o else 'meme.jpg')

    print(color(f'Meme saved to {o}.', fgc=2))
