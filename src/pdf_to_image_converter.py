"""
PDF to Image Converter Script.
"""

import argparse
import os
from pdf2image import convert_from_path


def convert_pdf_to_images(pdf_path, output_folder):
    """Convert a PDF file to images and save them in the output folder."""
    try:
        images = convert_from_path(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"{base_name}_page_{i+1}.png")
            image.save(image_path, "PNG")
        print(f"Converted {pdf_path} to images in {output_folder}")
    except FileNotFoundError as e:
        print(f"File not found: {pdf_path}. Error: {e}")
    except OSError as e:
        print(f"OS error while converting {pdf_path}: {e}")
    except ValueError as e:
        print(f"Value error converting {pdf_path}: {e}")


def process_pdfs(pdf_paths, output_folder):
    """Process a list of PDF file paths."""
    for pdf_path in pdf_paths:
        convert_pdf_to_images(pdf_path, output_folder)


def get_pdf_files_from_folder(folder):
    """Return a list of PDF file paths in the given folder."""
    return [
        os.path.join(folder, file)
        for file in os.listdir(folder)
        if file.lower().endswith(".pdf") and os.path.isfile(os.path.join(folder, file))
    ]


def main():
    """Main function to handle argument parsing and conversion logic."""
    parser = argparse.ArgumentParser(description="Convert PDF files to images.")
    parser.add_argument(
        "-f",
        "--file",
        help="Path to individual PDF file",
    )
    parser.add_argument(
        "-d",
        "--dir",
        help="Path to folder containing PDF files (default: pdf/)",
        default="pdf",
    )
    parser.add_argument(
        "-o", "--output", help="Output folder for images (default: img/)", default="img"
    )
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    if args.file:
        if os.path.isfile(args.file) and args.file.lower().endswith(".pdf"):
            process_pdfs([args.file], args.output)
        else:
            print("Invalid file path or not a PDF.")
    else:
        if os.path.exists(args.dir):
            pdf_files = get_pdf_files_from_folder(args.dir)
            if pdf_files:
                process_pdfs(pdf_files, args.output)
            else:
                print(f"No PDF files found in {args.dir}.")
        else:
            print(f"{args.dir}/ folder does not exist.")


if __name__ == "__main__":
    main()
