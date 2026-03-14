<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ManoGuzman/file-converter">
    <img src="https://img.icons8.com/?size=100&id=CoAutH1CZYoV&format=png&color=000000" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">File Converter</h3>

  <p align="center">
    A Python CLI utility to convert documents and images between popular file formats — PDF, Word, Markdown, JSON, and images.
    <br />
    <a href="https://github.com/ManoGuzman/file-converter"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ManoGuzman/file-converter/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/ManoGuzman/file-converter/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

`file-converter` is a command-line utility that converts documents and images between a variety of file formats. Each converter is a standalone Python script that supports both single-file and batch (directory) modes.

**Supported conversions:**

| Converter                   | Input                 | Output               |
| --------------------------- | --------------------- | -------------------- |
| `pdf_to_word_converter.py`  | PDF                   | DOCX (Word)          |
| `word_to_md_converter.py`   | DOCX / DOC            | Markdown             |
| `pdf_to_json_converter.py`  | PDF                   | JSON (text + tables) |
| `image_to_pdf_converter.py` | PNG / JPG / BMP / GIF | PDF                  |
| `pdf_to_image_converter.py` | PDF                   | PNG (one per page)   |

The project also ships two print-optimized CSS stylesheets (`styles/word-style.css` and `styles/kindle-style.css`) for use with the VS Code `markdown-pdf` extension, enabling a clean Markdown → PDF workflow.

**Default directory conventions** (relative to project root):

| Directory | Purpose               |
| --------- | --------------------- |
| `pdf/`    | Input PDFs            |
| `docs/`   | Output Word documents |
| `md/`     | Output Markdown files |
| `json/`   | Output JSON files     |
| `img/`    | Input/output images   |

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![pdf2docx][pdf2docx-badge]][pdf2docx-url]
* [![pypandoc][pypandoc-badge]][pypandoc-url]
* [![PyMuPDF][pymupdf-badge]][pymupdf-url]
* [![pdfplumber][pdfplumber-badge]][pdfplumber-url]
* [![python-docx][python-docx-badge]][python-docx-url]
* [![pypdf][pypdf-badge]][pypdf-url]
* [![pdf2image][pdf2image-badge]][pdf2image-url]
* [![Pillow][pillow-badge]][pillow-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

- **Python 3.10+** (uses `match`/`case` syntax)
- **[Pandoc](https://pandoc.org/installing.html)** — required for `word_to_md_converter.py`
- **[Poppler](https://poppler.freedesktop.org/)** — required for `pdf_to_image_converter.py`

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/ManoGuzman/file-converter.git
   cd file-converter
   ```

2. Install the package and its dependencies
   ```sh
   pip install -e .
   ```

3. (Optional) Install dev dependencies for linting and packaging
   ```sh
   pip install ".[dev]"
   ```

4. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### PDF → Word (DOCX)

```sh
# Single file — output goes to docs/
python src/pdf_to_word_converter.py -f "path/to/file.pdf"

# Batch — all PDFs in pdf/ → docs/
python src/pdf_to_word_converter.py -d
```

### Word → Markdown

```sh
# Single file
python src/word_to_md_converter.py -f input.docx [output.md]

# Batch folder (default: docs/ → md/)
python src/word_to_md_converter.py -d [input_folder] [output_folder]
```

### PDF → JSON

```sh
# Single file — output goes to json/
python src/pdf_to_json_converter.py -f "path/to/file.pdf"

# Batch — all PDFs in pdf/ → json/
python src/pdf_to_json_converter.py -d
```

The JSON output has the shape:
```json
{
  "text": "...",
  "tables": [{"col1": "val1", "col2": "val2"}, ...]
}
```

### Image → PDF

```sh
# Single image or folder of images — output goes to pdf/
python src/image_to_pdf_converter.py -f "path/to/image_or_folder"

# Default: reads from img/, outputs to pdf/output.pdf
python src/image_to_pdf_converter.py
```

Supported image formats: PNG, JPG, JPEG, BMP, GIF. Multiple images are combined into a single PDF.

### PDF → Images

```sh
# Single PDF — one PNG per page
python src/pdf_to_image_converter.py -f "path/to/file.pdf" [-o output_folder]

# Batch folder (default: pdf/ → img/)
python src/pdf_to_image_converter.py -d [folder] [-o output_folder]
```

### Running Tests

```sh
pytest
```

### Running Linter

```sh
ruff check src/
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] PDF to Word converter
- [x] Word to Markdown converter
- [x] PDF to JSON converter
- [x] Image to PDF converter
- [x] PDF to Image converter
- [ ] CLI entry point / unified command (`file-converter convert ...`)
- [ ] GUI or web interface
- [ ] Additional format support (EPUB, HTML, XLSX)

See the [open issues](https://github.com/ManoGuzman/file-converter/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/ManoGuzman/file-converter/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ManoGuzman/file-converter" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Manuel Guzmán - manuguzman8@gmail.com

Project Link: [https://github.com/ManoGuzman/file-converter](https://github.com/ManoGuzman/file-converter)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [pdf2docx](https://github.com/dothinking/pdf2docx)
* [pypandoc](https://github.com/JessicaTegner/pypandoc)
* [pdfplumber](https://github.com/jsvine/pdfplumber)
* [pdf2image](https://github.com/Belval/pdf2image)
* [Pillow](https://python-pillow.org/)
* [Pandoc](https://pandoc.org/)
* [Poppler](https://poppler.freedesktop.org/)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ManoGuzman/file-converter.svg?style=for-the-badge
[contributors-url]: https://github.com/ManoGuzman/file-converter/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ManoGuzman/file-converter.svg?style=for-the-badge
[forks-url]: https://github.com/ManoGuzman/file-converter/network/members
[stars-shield]: https://img.shields.io/github/stars/ManoGuzman/file-converter.svg?style=for-the-badge
[stars-url]: https://github.com/ManoGuzman/file-converter/stargazers
[issues-shield]: https://img.shields.io/github/issues/ManoGuzman/file-converter.svg?style=for-the-badge
[issues-url]: https://github.com/ManoGuzman/file-converter/issues
[license-shield]: https://img.shields.io/github/license/ManoGuzman/file-converter.svg?style=for-the-badge
[license-url]: https://github.com/ManoGuzman/file-converter/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/manuel-guzmán-b87b841bb
[product-screenshot]: images/screenshot.png
<!-- Shields.io badges -->
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[pdf2docx-badge]: https://img.shields.io/badge/pdf2docx-0.5.8+-blue?style=for-the-badge
[pdf2docx-url]: https://github.com/dothinking/pdf2docx
[pypandoc-badge]: https://img.shields.io/badge/pypandoc-1.6.4+-blue?style=for-the-badge
[pypandoc-url]: https://github.com/JessicaTegner/pypandoc
[pymupdf-badge]: https://img.shields.io/badge/PyMuPDF-1.24.0+-blue?style=for-the-badge
[pymupdf-url]: https://pymupdf.readthedocs.io/
[pdfplumber-badge]: https://img.shields.io/badge/pdfplumber-0.10.0+-blue?style=for-the-badge
[pdfplumber-url]: https://github.com/jsvine/pdfplumber
[python-docx-badge]: https://img.shields.io/badge/python--docx-1.1.0+-blue?style=for-the-badge
[python-docx-url]: https://python-docx.readthedocs.io/
[pypdf-badge]: https://img.shields.io/badge/pypdf-4.0.0+-blue?style=for-the-badge
[pypdf-url]: https://github.com/py-pdf/pypdf
[pdf2image-badge]: https://img.shields.io/badge/pdf2image-1.17.0+-blue?style=for-the-badge
[pdf2image-url]: https://github.com/Belval/pdf2image
[pillow-badge]: https://img.shields.io/badge/Pillow-10.0.0+-blue?style=for-the-badge
[pillow-url]: https://python-pillow.org/
