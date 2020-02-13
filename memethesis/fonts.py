from os import path

FONTS = {
    'notosans': 'NotoSans-Regular.ttf',
    'notosansmono': 'NotoSansMono-Regular.ttf',
    'impact': 'Impact.ttf',
    'comicsans': 'ComicSans.ttf'
}

IMPLY_STROKE = ['impact']

def get_fontpath(name: str):
    return path.join(
        path.dirname(__file__),
        'meme/res/fonts',
        FONTS[name.lower()]
    )
