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

## Help

### Installing

```
$ cd ~ # use $HOME
$ git clone https://github.com/fakefred/memethesis-cli # will clone the git repo
$ cd memethesis-cli # will go into directory
$ python3 setup.py bdist_wheel  # will generate .whl
$ pip3 install dist/memethesis* # will install the newly-created memethesis.whl created above
```

### Usage

> This part assumes you have a working python 3.x environment,
> which `python` refers to. If your OS uses `python3`, you are smart enough.

```
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

## Guide for new formats

`cd` to `./memethesis/meme/res/template`. Create a directory named after your
meme. Create `format.yml` inside the dir you created.

### `formats.yml`

#### Canonical documentation

```yml
# Keywords wrapped in <square brackets> are to be modified on demand;
# others are hardcoded. Starred (*) keywords are optional.
<name>:  # The flag you use for the meme format
# For example, if you name it 'drake' it is accessed via '-f drake'
  composition: vertical|horizontal|single
  # Denotes how the meme is made: stacked top to bottom,
  # laid side by side, or a single panel
  # Respective examples: drake, womanyelling, pigeon
  panels:
    # ^ When composition == 'single', things put here
    # are textboxes instead of panels, which are pasted on one panel
    <name>:  # < Flag for this panel/textbox
    # For example, if you named your panel/textbox 'dislike'
    # it is accessed via '--dislike <text>'
    # Make your panel/textbox as unique as possible,
    # and if you can, make it short and descriptive.
    # IMPORTANT: flag names CAN collide. Make your flag different from
    # all others.
      description*: <description>
      # ^ Shown in --list and, if the composition is not single,
      # in --interactive
      image: <dir>/<image>
      # ^ Image path relative to ./memethesis/meme/res/template/
      textbox: [370, 12, 400, 250]
      # ^ Textbox position, in left, top, width, height
      font*: notosans|notosansmono|impact|comicsans
      # ^ Default font for the template
      # (memethesis assumes notosans if none; see `fonts.py`)
      # Overridden when '--font' is specified in command mode
      style*: stroke
      # ^ Use 'stroke' if default font is impact for best effects
    <name>:
      # ...
    # ...
<name>:  # You can combine multiple templates into one dir,
# but only do that when they're relevant and inseparable
# ...
```

#### Example

Here is an tested example, from the drake format:

```yml
drake:
  composition: vertical
  panels:
    dislike:
      description: Drake dislike
      image: drake/drake_dislike.jpg
      textbox: [370, 12, 400, 250]
    like:
      description: Drake like
      image: drake/drake_like.jpg
      textbox: [370, 20, 400, 250]
```

Here are a few points to follow:

- Make the directory and files distinguishable from others or potential ones:
  for example, `spiderman` serves as a poor identifier for meme formats because there are countless spiderman memes.
- Keep the image resolution moderately high. 800px wide is enough.
  Don't scale up too much.
- Don't include whitespace in filenames and yml keywords.
- Use lower case as default, unless capital ones are necessary.
- Test before opening a PR. Ensure the textboxes are right by feeding it long
  strings like `'mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm'`.
  I will clone your fork and test personally.
- If you ensure the test passes, add a command you use to test your format to
  `test.sh` in the root dir of the project.

## Debugging

```bash
[make edits]
# to test by running module
$ python -m memethesis.__main__ [args]
# to test all formats with shell script
$ sudo chmod +x test.sh
$ ./test.sh
# to test by installing wheel
$ python setup.py bdist_wheel  # will generate .whl
$ pip install dist/memethesis-[something].whl
```
