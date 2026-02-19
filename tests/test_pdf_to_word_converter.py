# tests/test_pdf_to_word_converter.py
"""
Unit tests for the pdf_to_word_converter module.
"""

import os
import tempfile
from pathlib import Path

import pytest

from src.pdf_to_word_converter import (
    is_file_readable,
    validate_file_has_extension,
    validate_file_not_empty,
    validate_input_directory,
    validate_is_directory,
    validate_is_file,
    validate_output_directory_exists,
    validate_output_file,
    validate_path_exists,
    validate_pdf_input_file,
)


class TestValidationFunctions:
    """Test class for PDF to Word converter validation functions."""

    def test_is_file_readable(self):
        """Test that is_file_readable returns True for readable files."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = Path(tmp.name)
            assert is_file_readable(tmp_path)
        os.unlink(tmp_path)

        # Non-existent file
        assert not is_file_readable(Path("nonexistent.txt"))

    def test_validate_path_exists(self):
        """Test validate_path_exists raises for non-existent paths."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # Should not raise
            validate_path_exists(tmp_path, "test")

        with pytest.raises(FileNotFoundError):
            validate_path_exists(Path("nonexistent"), "test")

    def test_validate_is_file(self):
        """Test validate_is_file for files and directories."""
        with tempfile.NamedTemporaryFile() as tmp:
            tmp_path = Path(tmp.name)
            # Should not raise
            validate_is_file(tmp_path)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            with pytest.raises(ValueError):
                validate_is_file(tmp_path)

    def test_validate_is_directory(self):
        """Test validate_is_directory for directories and files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # Should not raise
            validate_is_directory(tmp_path)

        with tempfile.NamedTemporaryFile() as tmp:
            tmp_path = Path(tmp.name)
            with pytest.raises(ValueError):
                validate_is_directory(tmp_path)

    def test_validate_file_not_empty(self):
        """Test validate_file_not_empty for empty and non-empty files."""
        # Non-empty file should not raise
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"content")
            tmp.flush()
            tmp_path = Path(tmp.name)
            validate_file_not_empty(tmp_path)

        # Empty file should raise ValueError
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = Path(tmp.name)
        with pytest.raises(ValueError):
            validate_file_not_empty(tmp_path)

    def test_validate_file_has_extension(self):
        """Test validate_file_has_extension for correct and incorrect extensions."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            # Should not raise
            validate_file_has_extension(tmp_path, ".pdf")
        os.unlink(tmp_path)

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            with pytest.raises(ValueError):
                validate_file_has_extension(tmp_path, ".pdf")
        os.unlink(tmp_path)

    def test_validate_pdf_input_file(self):
        """Test validate_pdf_input_file for valid and invalid PDF files."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(b"dummy pdf content")
            tmp.flush()  # Ensure content is written to disk
            tmp_path = Path(tmp.name)
        result = validate_pdf_input_file(str(tmp_path))
        assert result == tmp_path
        os.unlink(tmp_path)

        # Invalid extension
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            with pytest.raises(ValueError):
                validate_pdf_input_file(str(tmp_path))
        os.unlink(tmp_path)

    def test_validate_input_directory(self):
        """Test validate_input_directory for directories with and without PDFs."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # Create a dummy PDF
            pdf_path = tmp_path / "test.pdf"
            pdf_path.write_bytes(b"dummy")

            result_path, pdf_files = validate_input_directory(str(tmp_path))
            assert result_path == tmp_path
            assert len(pdf_files) == 1
            assert pdf_files[0] == pdf_path

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # No PDFs
            with pytest.raises(ValueError):
                validate_input_directory(str(tmp_path))

    def test_validate_output_directory_exists(self):
        """Test validate_output_directory_exists creates directories if needed."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            result = validate_output_directory_exists(str(tmp_path))
            assert result == tmp_path

        # Non-existent directory should be created
        with tempfile.TemporaryDirectory() as base_dir:
            new_dir = Path(base_dir) / "new_output"
            result = validate_output_directory_exists(str(new_dir))
            assert result == new_dir
            assert new_dir.exists()

    def test_validate_output_file(self):
        """Test validate_output_file for valid output paths."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            output_file = tmp_path / "output.docx"
            result = validate_output_file(output_file)
            assert result == output_file

        # Wrong extension (should warn but not raise)
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            output_file = tmp_path / "output.txt"
            result = validate_output_file(output_file)
            assert result == output_file
