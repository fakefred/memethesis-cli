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

### Usage

```bash
$ memethesis -i  # interactive mode (try it)
$ memethesis -h
usage: __main__.py [-h] [-i]
                   [-f {drake,brainsize,womanyelling,pooh,pigeon,draw25}]
                   [-o OUTPUT] [-p] [-c CAPTION]
                   [--dislike DISLIKE] [--like LIKE]
                   [--s1 S1] [--s2 S2] [--s3 S3] [--s4 S4]
                   [--s5 S5] [--s6 S6] [--s7 S7] [--s8 S8]
                   [--s9 S9] [--s10 S10] [--s11 S11]
                   [--s12 S12] [--s13 S13] [--s14 S14]
                   [--woman WOMAN] [--cat CAT]
                   [--tired TIRED] [--wired WIRED]
                   [--katori KATORI] [--butterfly BUTTERFLY]
                   [--is-this-a IS_THIS_A] [--do DO]
                   [--guy GUY]

All Your Memes Are Belong To Us!

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     interactive mode
  -f {drake,brainsize,womanyelling,pooh,pigeon,draw25}, --format {drake,brainsize,womanyelling,pooh,pigeon,draw25}
                        the meme format to use (Supported:
                        drake, brainsize, womanyelling, pooh,
                        pigeon, draw25)
  -o OUTPUT, --output OUTPUT
                        the filename to save the meme as
                        (default: ./meme.jpg)
  -p, --preview         display the meme without saving it,
                        unless -o/--output is specified
  -c CAPTION, --caption CAPTION
                        caption text to add above your meme

drake:
  --dislike DISLIKE
  --like LIKE

brainsize:
  --s1 S1
  --s2 S2
  ...
  --s14 S14

womanyelling:
  --woman WOMAN
  --cat CAT

pooh:
  --tired TIRED
  --wired WIRED

pigeon:
  --katori KATORI
  --butterfly BUTTERFLY
  --is-this-a IS_THIS_A

draw25:
  --do DO
  --guy GUY
```
