"""
PDF to JSON Converter Script.
"""

import os
import argparse
import json
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


# Function to extract text from PDF
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
    except PdfReadError as e:
        print(f"PDF read error: {e}")
        return ""


# Function to convert PDF to JSON
def convert_pdf_to_json(pdf_file_path, json_file_path):
    """
    Converts a PDF file to a JSON file containing the extracted text.
    """
    try:
        text = extract_text_from_pdf(pdf_file_path)
        data = {"text": text}
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except IOError as e:
        print(f"I/O error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to JSON.")
    parser.add_argument(
        "pdf_file", nargs="?", help="Path to the PDF file (default: pdf/<filename>.pdf)"
    )
    parser.add_argument(
        "output_json",
        nargs="?",
        help="Path to the output JSON file (default: json/<filename>.json)",
    )
    args = parser.parse_args()

    # Default folders
    PDF_FOLDER = "pdf"
    JSON_FOLDER = "json"

    # Determine PDF file path
    if args.pdf_file:
        pdf_path = args.pdf_file
        PDF_FILENAME = os.path.splitext(os.path.basename(pdf_path))[0]
    else:
        PDF_FILENAME = "input"
        pdf_path = os.path.join(PDF_FOLDER, f"{PDF_FILENAME}.pdf")

    # Determine JSON output path
    if args.output_json:
        json_path = args.output_json
    else:
        json_path = os.path.join(JSON_FOLDER, f"{PDF_FILENAME}.json")

    # Ensure output folder exists
    os.makedirs(JSON_FOLDER, exist_ok=True)

    convert_pdf_to_json(pdf_path, json_path)
    print(f"Converted '{pdf_path}' to '{json_path}' successfully.")
