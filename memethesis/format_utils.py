import yaml
from os import path
from .fancyprint import color
import sys


def read_formats() -> dict:
    try:
        return yaml.load(
            open(path.join(path.dirname(__file__), 'meme/formats.yml')),
            Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(color(
            f'Error: {path.join(path.dirname(__file__), "meme/formats.yml")} not found.',
            fgc=1))  # red
        sys.exit(1)


def get_format_names(fmts: dict) -> list:
    return list(fmts.keys())


def get_panel_types(fmts: dict) -> dict:
    return {k: list(v['panels'].keys()) for k, v in fmts.items()}


def get_panel_descriptions(fmts: dict) -> dict:
    descrips = {
        fk: {
            pk: pv['description']
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
