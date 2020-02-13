# memethesis-cli

![Upload Python Package](https://github.com/fakefred/memethesis-cli/workflows/Upload%20Python%20Package/badge.svg) <a href="https://liberapay.com/fakefred/donate"><img alt="Donate using Liberapay" src="http://img.shields.io/liberapay/receives/fakefred.svg?logo=liberapay"></a>

## Updates in 3.0.0-beta

Automation has reached a new level where **all** existing formats are fully
automated by memethesizers for their respective compositions,
including `single`, `vertical`, and `horizontal`.
Adding new formats are now easier than ever,
which is why this repo is open to issues and PR's for new formats,
instead of the author writing new scripts for each one of them because
everyone has limited energy.
If you would like a new format and could afford the time and effort to provide
the data, please open a PR;
if you cannot, open an issue.
The former type of contributors should pay attention to such issues,
and help with them when possible.

## Guide for new formats

Just stuff in metadata into `memethesis/meme/formats.yml` and images into
`memethesis/meme/res/template/[template_name]/[image_name]`.
Here are a few points to follow:

- Make the directory and files distinguishable from others or potential ones:
  for example, `spiderman` serves as a poor identifier for meme formats because there
  are countless spiderman memes.
- Keep the image resolution moderately high. 800px wide is enough.
  Don't scale up too much.
- Use underscores(`_`).
- Use lower case as default, unless capital ones are necessary.
- Update aforementioned `formats.yml` with reference to existing formats if possible.
  When in doubt, consult people who have submitted new formats in the yml.
- Test before opening a PR. Ensure the textboxes are right by feeding it long
  strings like `'mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm'`.
  I will clone your fork and test personally.

## Help

### Installing

```bash
$ pip install memethesis
```

Or when updating:

```bash
$ pip install memethesis==<latest_version> --upgrade
```

Installing from git repository:

```bash
$ python setup.py bdist_wheel  # will generate .whl
$ pip install dist/memethesis-[something].whl
```

### Usage

> This part assumes you have a working python 3.x environment,
> which `python` refers to. If your OS uses `python3`, you are smart enough.

```bash
$ memethesis -h
Memethesis CLI - All Your Memes Are Belong To Us!

arguments:
  -h, --help            show this help message and exit
  -l, --list            show a list of meme formats and exit
  -i, --interactive     interactive mode (certain formats only)

  -f, --format FORMAT   the meme format to use
  -c, --caption CAPTION caption text to add above your meme
  --font FONT           the font to use for body panels

  -o, --output OUTPUT   save the meme as (jpg/png)
  -p, --preview         display meme without saving it,
                        unless -o/--output is specified

usage:
  # command mode
  $ memethesis -f FORMAT [-p|-o filename] --flag0 TEXT0 --flag1 TEXT1 ...

  # remember to wrap spaced strings in quotes
  # example:
  $ memethesis -f drake -o meme.png --dislike 'one thing' --like 'another thing'

  # interactive mode
  $ memethesis -i
```

## Debugging

```bash
[make edits]
# to test by running module
$ python -m memethesis.__main__ [args]
# to test by installing wheel
$ python setup.py bdist_wheel  # will generate .whl
$ pip install dist/memethesis-[something].whl
```
