import yaml
from os import path, listdir
from .fancyprint import color
import sys


def read_formats() -> dict:
    # template metadata are stored in
    # ./res/template/<template_name>/format.yml
    templates = {}
    temp_path = path.join(path.dirname(__file__), 'meme/res/template')
    temp_dirs = listdir(temp_path)
    for temp in temp_dirs:
        try:
            fmt = yaml.load(
                open(path.join(temp_path, temp, 'format.yml')),
                Loader=yaml.FullLoader)
            for k, v in fmt.items():
                templates[k] = v
        except FileNotFoundError:
            print(color(
                f'Warning: no format.yml found for meme format `{temp}`.',
                fgc=3))  # yellow
            continue

    if templates:
        return templates

    print(color('No meme formats found.', fgc=1))
    sys.exit(1)


def get_format_names(fmts: dict) -> list:
    return list(fmts.keys())


def get_panel_types(fmts: dict) -> dict:
    return {k: list(v['panels'].keys()) for k, v in fmts.items()}


def get_panel_descriptions(fmts: dict) -> dict:
    descrips = {
        fk: {
            pk: pv['description'] if 'description' in pv else ''
            for pk, pv in fv['panels'].items()
        } for fk, fv in fmts.items()
    }

    for fk in descrips.keys():
        descrips[fk]['caption'] = 'Caption'
        descrips[fk]['sep'] = 'Horizontal line'
        descrips[fk]['abort'] = '[stop adding panels]'

    return descrips


def get_compositions(fmts: dict) -> dict:
    return {k: v['composition'] for k, v in fmts.items()}
