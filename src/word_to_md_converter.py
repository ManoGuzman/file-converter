"""
Word to Markdown Converter Script.

This module provides functionality to convert Word documents (.docx, .doc)
to Markdown format using pypandoc and Pandoc.
"""

import sys
from pathlib import Path
from typing import Optional

try:
    import pypandoc
except ImportError:
    print(
        "Error: 'pypandoc' module not installed. "
        "Install with 'pip install pypandoc'."
    )
    sys.exit(1)

# Constants for error messages
ERROR_MESSAGES = {
    "pypandoc": (
        "Error: The 'pypandoc' module is not installed. "
        "Please install it with 'pip install pypandoc'"
    ),
    "pandoc": (
        "Error: Pandoc binary not found. "
        "Please install Pandoc from https://pandoc.org/installing.html."
    ),
    "file_not_found": "Input file not found: {0}",
    "folder_not_found": "Input folder not found: {0}",
    "invalid_extension": "Input file must be a Word document (.docx or .doc)",
    "usage": (
        "Usage:\n"
        "  Single file: python src/convert_word_to_md.py -f <input_file.docx> [output_file.md]\n"
        "  Batch folder: python src/convert_word_to_md.py -d <input_folder> [output_folder]"
    ),
    "dir_creation_failed": "Failed to create output directory {0}: {1}",
    "file_operation_failed": "File operation error converting {0}: {1}",
    "conversion_failed": "Pandoc conversion error for {0}: {1}",
}

VALID_EXTENSIONS = {".docx", ".doc"}

# Default paths
DEFAULT_DOCS_FOLDER = Path(__file__).parent.parent / "docs"
DEFAULT_OUTPUT_FOLDER = Path(__file__).parent.parent / "md"

# Valid mode flags
FILE_MODE_FLAGS = {"-f", "--file"}
DIR_MODE_FLAGS = {"-d", "--dir"}


def check_pandoc_installation() -> None:
    """Check if Pandoc is installed and raise an error if not."""
    if not pypandoc.get_pandoc_path():
        print(ERROR_MESSAGES["pandoc"])
        sys.exit(1)


def create_directory_if_needed(directory: Path) -> None:
    """
    Create a directory if it doesn't exist.

    Args:
        directory: Path to the directory

    Raises:
        OSError: If directory creation fails
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(ERROR_MESSAGES["dir_creation_failed"].format(directory, e)) from e


def validate_path(path: Path, is_file: bool = True) -> None:
    """
    Validate that a path exists and is of the correct type.

    Args:
        path: Path to validate
        is_file: If True, validates as file; if False, validates as directory

    Raises:
        FileNotFoundError: If path doesn't exist or is wrong type
        ValueError: If file extension is invalid (for files only)
    """
    if is_file:
        if not path.exists():
            raise FileNotFoundError(ERROR_MESSAGES["file_not_found"].format(path))
        if path.suffix.lower() not in VALID_EXTENSIONS:
            raise ValueError(ERROR_MESSAGES["invalid_extension"])
    else:
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(ERROR_MESSAGES["folder_not_found"].format(path))


def convert_word_to_markdown(input_file: Path, output_file: Path) -> None:
    """
    Convert a Word document to Markdown format.

    Args:
        input_file: Path to the input Word file (.docx or .doc)
        output_file: Path to the output Markdown file

    Raises:
        RuntimeError: If conversion fails
        OSError: If file operations fail
    """
    try:
        pypandoc.convert_file(str(input_file), "md", outputfile=str(output_file))
        print(f"✓ Converted: {input_file.name} -> {output_file}")
    except (OSError, IOError) as e:
        raise RuntimeError(
            ERROR_MESSAGES["file_operation_failed"].format(input_file, e)
        ) from e
    except RuntimeError as e:
        raise RuntimeError(
            ERROR_MESSAGES["conversion_failed"].format(input_file, e)
        ) from e


def get_output_path(input_path: Path, output_file: Optional[str]) -> Path:
    """
    Determine the output path for a converted file.

    Args:
        input_path: Path to the input file
        output_file: Optional output file path

    Returns:
        Path object for the output file
    """
    if output_file:
        return Path(output_file)

    output_path = DEFAULT_OUTPUT_FOLDER / input_path.with_suffix(".md").name
    create_directory_if_needed(output_path.parent)
    return output_path


def convert_single_file(input_file: str, output_file: Optional[str] = None) -> None:
    """
    Convert a single Word document to Markdown.

    Args:
        input_file: Path to the input Word file
        output_file: Path to the output Markdown file.
                    If None, uses default output folder with same filename

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If file extension is invalid
        RuntimeError: If conversion fails
        OSError: If file operations fail
    """
    input_path = Path(input_file)
    validate_path(input_path, is_file=True)
    output_path = get_output_path(input_path, output_file)

    check_pandoc_installation()
    convert_word_to_markdown(input_path, output_path)


def convert_folder(
    input_folder: Optional[str] = None, output_folder: Optional[str] = None
) -> None:
    """
    Convert all Word documents in a folder to Markdown.

    Args:
        input_folder: Path to the input folder.
                     If None, uses default docs folder
        output_folder: Path to the output folder.
                      If None, uses default md folder

    Raises:
        FileNotFoundError: If input folder doesn't exist
        OSError: If output folder creation fails
    """
    input_path = Path(input_folder) if input_folder else DEFAULT_DOCS_FOLDER
    output_path = Path(output_folder) if output_folder else DEFAULT_OUTPUT_FOLDER

    validate_path(input_path, is_file=False)
    create_directory_if_needed(output_path)
    check_pandoc_installation()

    # Find all Word files
    word_files = [f for ext in VALID_EXTENSIONS for f in input_path.glob(f"*{ext}")]

    if not word_files:
        print(f"No Word files found in {input_path}")
        return

    print(f"Found {len(word_files)} file(s) to convert...")

    converted = 0
    failed = 0

    for word_file in word_files:
        try:
            output_file = output_path / word_file.with_suffix(".md").name
            convert_word_to_markdown(word_file, output_file)
            converted += 1
        except (RuntimeError, OSError, IOError) as e:
            print(f"✗ Failed: {word_file.name} - {e}")
            failed += 1

    print(f"\nConversion complete: {converted} successful, {failed} failed")


# Main function
def main() -> None:
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print(ERROR_MESSAGES["usage"])
        sys.exit(1)

    mode = sys.argv[1]

    try:
        if mode in FILE_MODE_FLAGS:
            if len(sys.argv) < 3:
                print("Error: Input file required for file mode")
                print(ERROR_MESSAGES["usage"])
                sys.exit(1)

            input_file = sys.argv[2]
            output_file = sys.argv[3] if len(sys.argv) > 3 else None
            convert_single_file(input_file, output_file)

        elif mode in DIR_MODE_FLAGS:
            input_folder = sys.argv[2] if len(sys.argv) > 2 else None
            output_folder = sys.argv[3] if len(sys.argv) > 3 else None
            convert_folder(input_folder, output_folder)

        else:
            print(f"Error: Invalid mode '{mode}'")
            print(ERROR_MESSAGES["usage"])
            sys.exit(1)

    except (FileNotFoundError, ValueError, RuntimeError, OSError) as e:
        print(f"Error: {e}")
        sys.exit(1)


# Entry point
if __name__ == "__main__":
    main()
