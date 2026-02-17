# File Converter &middot; [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/ManoGuzman/file-converter/blob/master/LICENSE)

<img src="https://img.icons8.com/?size=100&id=CoAutH1CZYoV&format=png&color=000000" alt="file converter" align="right" width="125" height="125">

> Simple and extensible file conversion utility for Windows

A command-line Python tool to convert files between different formats (PDF to Word, Word to Markdown, etc.). Useful for quick document transformations and automation.

## Installing / Getting started

Clone the repository and install dependencies:

```shell
git clone https://github.com/ManoGuzman/file-converter.git
cd file-converter

python -m venv venv
venv\Scripts\activate  # On Windows

pip install -r requirements.txt
```

This will set up the project locally and install all required Python dependencies.

## Usage

Convert a PDF to Word:

```shell
python src/pdf_to_word_converter.py -f path/to/input.pdf
```

Convert all PDFs in the default folder:j

```shell
python src/pdf_to_word_converter.py -d
```

Convert a Word document to Markdown:

```shell
python src/word_to_md_converter.py -f path/to/input.docx
```

See each script's help or source for more options.

## Developing

### Built With

- Python 3.10+
- [pdf2docx](https://pypi.org/project/pdf2docx/) for PDF to Word
- [pypandoc](https://pypi.org/project/pypandoc/) for Word to Markdown
- [pdfplumber](https://pypi.org/project/pdfplumber/) and [python-docx](https://pypi.org/project/python-docx/) for alternative PDF conversion

### Prerequisites

- [Python](https://www.python.org/) 3.10 or higher
- [pip](https://pip.pypa.io/en/stable/)
- (Optional) [pnpm](https://pnpm.io/) if you use Node.js tools for linting or formatting

### Setting up Dev

- Clone the repository:

```shell
git clone https://github.com/ManoGuzman/file-converter.git
cd file-converter
```

- Create and activate a virtual environment:

```shell
python -m venv venv
venv\Scripts\activate  # On Windows
```

- Install dependencies:

```shell
pip install -r requirements.txt
```

- Run the scripts in the `src` folder with your files.

No database or server setup is required.

### Building

No build step is required for this project. The scripts can be run directly with Python.

### Deploying / Publishing

To release a new version, tag your commit and push to the repository. If distributing via PyPI, use:

```shell
python setup.py sdist bdist_wheel
pip install twine
twine upload dist/*
```

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. See the [tags on this repository](https://github.com/ManoGuzman/file-converter/tags) for available versions.

## Configuration

You can configure the following options via CLI flags (see each script for details):

- `-f, --file`: Path to the input file.
- `-d, --dir`: Path to the input directory.
- Output paths and formats are script-dependent.

## Tests

To run tests (if available):

```shell
pytest
```

Tests cover core conversion logic and CLI argument parsing.

## Style guide

- Follows [PEP8](https://peps.python.org/pep-0008/) code style.
- To check style:

```shell
flake8 .
```

## API Reference

This is a CLI tool. For programmatic usage, import the conversion functions from the scripts in `src/`.

## Database

No database is used in this project.

## Licensing

MIT License. See [LICENSE](./LICENSE) for details.
