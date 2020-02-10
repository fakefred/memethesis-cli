from colored import fg, attr
# color chart see https://pypi.org/project/colored/


def color(text: str, fgc=15):
    return f'{fg(fgc)}{text}{attr(0)}'


def style(text: str, sty=0):
    return f'{attr(sty)}{text}{attr(0)}'
