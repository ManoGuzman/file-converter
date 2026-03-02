"""
PDF to JSON Converter Script.
"""

import sys
import json
import pathlib
import pdfplumber

from pypdf import PdfReader
from pypdf.errors import PdfReadError


PDF_EXTENSION = ".pdf"
JSON_EXTENSION = ".json"
DEFAULT_PDF_DIR = "pdf"
DEFAULT_JSON_DIR = "json"


def extract_text_from_pdf(pdf_file_path):
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(pdf_file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return ""
    except PdfReadError as e:
        print(f"PDF read error: {e}")
        return ""


def extract_tables_from_pdf(pdf_file_path):
    """Extract tables from a PDF file and return as a list of dicts."""
    tables = []
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                for table in page_tables:
                    # Assume first row is header
                    headers = table[0]
                    for row in table[1:]:
                        row_dict = {headers[i]: row[i] for i in range(len(headers))}
                        tables.append(row_dict)
        return tables
    except (
        FileNotFoundError,
        pdfplumber.pdfminer.pdfparser.PDFSyntaxError,
        IOError,
    ) as e:
        print(f"Error extracting tables: {e}")
        return []


def convert_pdf_to_json(pdf_file_path, json_file_path):
    """Converts a PDF file to a JSON file containing extracted text and tables."""
    text = extract_text_from_pdf(pdf_file_path)
    tables = extract_tables_from_pdf(pdf_file_path)
    data = {"text": text, "tables": tables}
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def validate_pdf_file(pdf_file: pathlib.Path) -> pathlib.Path:
    """Validate that the given path is a readable PDF file."""
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_file}")
    if not pdf_file.is_file():
        raise ValueError(f"Path is not a file: {pdf_file}")
    if pdf_file.suffix.lower() != PDF_EXTENSION:
        raise ValueError(f"File must have .pdf extension: {pdf_file}")
    return pdf_file


def validate_directory(directory: pathlib.Path) -> pathlib.Path:
    """Validate that the given path is a directory."""
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not directory.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    return directory


def convert_single_pdf(pdf_path: str, json_dir: str):
    """Convert a single PDF file to JSON."""
    pdf_file = validate_pdf_file(pathlib.Path(pdf_path))
    json_dir_path = pathlib.Path(json_dir)
    json_dir_path.mkdir(parents=True, exist_ok=True)
    json_file = json_dir_path / (pdf_file.stem + JSON_EXTENSION)
    convert_pdf_to_json(str(pdf_file), str(json_file))
    print(f"Converted '{pdf_file}' to '{json_file}' successfully.")


def convert_pdf_directory(pdf_dir: str, json_dir: str):
    """Convert all PDF files in a directory to JSON files."""
    pdf_dir_path = validate_directory(pathlib.Path(pdf_dir))
    json_dir_path = pathlib.Path(json_dir)
    json_dir_path.mkdir(parents=True, exist_ok=True)
    pdf_files = list(pdf_dir_path.glob(f"*{PDF_EXTENSION}"))
    if not pdf_files:
        print(f"No PDF files found in directory: {pdf_dir}")
        return
    print(f"Found {len(pdf_files)} PDF file(s) to convert.")
    converted = 0
    failed = 0
    for pdf_file in pdf_files:
        json_file = json_dir_path / (pdf_file.stem + JSON_EXTENSION)
        try:
            convert_pdf_to_json(str(pdf_file), str(json_file))
            print(f"✓ Converted '{pdf_file.name}' to '{json_file.name}'")
            converted += 1
        except (IOError, ValueError) as e:
            print(f"✗ Failed to convert '{pdf_file.name}': {e}")
            failed += 1
    print(f"\nConversion complete: {converted} successful, {failed} failed.")


def print_usage():
    """Print usage instructions for the CLI."""
    usage = """
PDF to JSON Converter

Usage:
  Mode 1 - Convert single file:
    python src/pdf_to_json_converter.py -f <input_pdf>
    Output: json/<filename>.json

  Mode 2 - Convert all PDFs in directory:
    python src/pdf_to_json_converter.py -d
    Input: pdf/
    Output: json/

Examples:
  python src/pdf_to_json_converter.py -f "C:\\path\\to\\file.pdf"
  python src/pdf_to_json_converter.py -d
"""
    print(usage)


def main():
    """Main entry point for the CLI."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    mode = sys.argv[1]
    try:
        match mode:
            case "-f" | "--file":
                if len(sys.argv) != 3:
                    print("Error: Mode -f requires an input PDF file")
                    print_usage()
                    sys.exit(1)
                input_pdf = sys.argv[2]
                convert_single_pdf(input_pdf, DEFAULT_JSON_DIR)
            case "-d" | "--directory":
                convert_pdf_directory(DEFAULT_PDF_DIR, DEFAULT_JSON_DIR)
            case _:
                print(f"Error: Unknown mode '{mode}'")
                print_usage()
                sys.exit(1)
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nConversion cancelled by user")
        sys.exit(130)


if __name__ == "__main__":
    main()
