# markup-export

This project is a wrapper around [Pandoc](https://pandoc.org/) that aims to help
organize and manage `yaml`-templates and ease & accelerate overall use of Pandoc.

## Features

### Templates

- everything [native Pandoc
  `yaml`-templates](https://pandoc.org/MANUAL.html#variables) can do
- include templates into other templates for modular structure and reusability
- specify Pandoc CLI options in templates
- sensible template presets for reference & quick start
- interactive template picker with tree structure

### Source files

- arbitrary numbers of `.md` and
  [bibliography](https://pandoc.org/MANUAL.html#specifying-bibliographic-data)
  files and directories are handled automatically

### Other

- only one Python dependency: `PyYAML`
- see [issues](https://github.com/jannis-baum/markup-export/issues) for planned
  features & feel free to add requests!

## Setup

- [install Pandoc](https://pandoc.org/installing.html)
- install requirements from `requirements.txt`, e.g. `/usr/bin/env python3 -m
  pip install -r requirements.txt`
- set up `.env` (`cp .env.example .env` and optionally modify to your liking)

## Usage

Execute `main` with `sources` as positional arguments. Sources can be files or
directories; all found `.md` files will be treated as textual content (sorted
alphabetically in traversing order) and all bibliography files will be added as
bibliographic references.

### Environment options

Specify environment variables before executing markup-export or set them in your
`.env` file.

- `CMD_EDITOR` is the command to run to open your editor. The string `{}` will
  be replaced with the file to edit. To use `vim` for example set
  `CMD_EDITOR=vim {}`
- `CMD_QUICKLOOK` is the command to run to quick-look / preview an exported
  file (again, given by `{}`). On MacOS you can use Finder's Quicklook action
  with `CMD_QUICKLOOK=qlmanage -p {} >& /dev/null`.
- If `QUICKLOOK_BY_DEFAULT` is set to one of `1`, `true`, `t`, `True` or `T`, an
  exported file will be previewed when the CLI argument `-q` is not given;
  otherwise it is the other way around.
- `TEMPLATE_DIR` specifies the (relative) *template directory* used to store
  template files.
- `TEMPLATE_RECENT` is the name the last used template is stored as in the
  *template directory*.

### Optional CLI arguments

- `-o FILENAME, --out FILENAME` to specify the output. This can be a `.pdf` or
  any other [output format supported by Pandoc](https://pandoc.org/MANUAL.html#general-options)
- `-t TEMPLATE, --template TEMPLATE` to specify the template to use. `TEMPLATE`
  is used to identify a template (`.yaml`-file) in the *template
  directory*. Templates in subdirectories, e.g. in `presets` are identified by
  preceding their name with the subdirectory's name, e.g. `presets/plain` for
  the given preset *Plain*. Note that a directory or file name's prefix is
  sufficient to identify it, i.e. `pre/pl` or even `p/p` would be enough to pick
  `presets/plain` if no other template matching this string exists.
- `-r, --recent` lets you use the last used template again.
- `-e [SAVE_AS], --edit [SAVE_AS]` lets you edit and optionally save the chosen
  template before using it for the export. It will open the template in your
  editor and, if `SAVE_AS` was given, save it with this name (subdirectories can
  be set with `/` separators) into your *template directory*.
- `-i, --interactive` is an alternative to `-t` and `-e`; it will display your
  templates as a tree and ask you to input a template analogous to the `-t`
  option. You can edit the template by suffixing the word `new` and save the
  edit with `new as SAVE_AS` analogously to the `-e` option.
- `-d, --debug` enables passing through `stdout` and `stderr` of Pandoc's
  subprocess which is useful for debugging your custom templates.
- `-q, --quicklook` reverses the behavior specified by the environment setting
  `QUICKLOOK_BY_DEFAULT`
