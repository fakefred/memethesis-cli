from ascim.ascim import ASCIM
from ascim.draw import ASCIMDraw
from ascim.tables import ASCIMTable
from ..format_utils import read_formats
from ..fancyprint import color
import sys


def make_ascii(format: str, entities: dict, cmdfont=None):
    format_info = read_formats()[format]
    panels_info = format_info['panels']
    for panel in panels_info.values():
        if not 'ascii' in panel or not 'asciibox' in panel:
            print(color('ASCII art template or textbox not found.', fgc=1))
            sys.exit(1)

    panels = []
    for name, text in entities:
        if name in panels_info:
            meta = panels_info[name]
            temp = ASCIM(meta['ascii'].strip())
            temp = temp.crop((1, 1, temp.size[0] - 2, temp.size[1] - 2))
            draw = ASCIMDraw(temp)
            draw.text(meta['asciibox'], text)
            panels.append(temp)
    comp = format_info['composition']
    if comp == 'vertical':
        table_data = [[p] for p in panels]
    elif comp in ('horizontal', 'single'):
        table_data = [panels]
    table = ASCIMTable(table_data)
    return table.to_text()
