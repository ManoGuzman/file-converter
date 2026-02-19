# tests/test_word_to_md_converter.py
"""
Unit tests for the word_to_md_converter module.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.word_to_md_converter import (
    check_pandoc_installation,
    create_directory_if_needed,
    get_output_path,
    validate_path,
)


class TestWordToMdConverter:
    """Test class for Word to Markdown converter functions."""

    def test_create_directory_if_needed(self):
        """Test that create_directory_if_needed creates a directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as base_dir:
            new_dir = Path(base_dir) / "new_dir"
            create_directory_if_needed(new_dir)
            assert new_dir.exists()
            assert new_dir.is_dir()

    def test_validate_path_file(self):
        """Test validate_path for files."""
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            # Should not raise
            validate_path(tmp_path, is_file=True)
        os.unlink(tmp_path)

        # Non-existent file
        with pytest.raises(FileNotFoundError):
            validate_path(Path("nonexistent.docx"), is_file=True)

        # Invalid extension
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            with pytest.raises(ValueError):
                validate_path(tmp_path, is_file=True)
        os.unlink(tmp_path)

    def test_validate_path_directory(self):
        """Test validate_path for directories."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # Should not raise
            validate_path(tmp_path, is_file=False)

        # Non-existent directory
        with pytest.raises(FileNotFoundError):
            validate_path(Path("nonexistent_dir"), is_file=False)

    def test_get_output_path_with_specified(self):
        """Test get_output_path with specified output file."""
        input_path = Path("input.docx")
        output_file = "output.md"
        result = get_output_path(input_path, output_file)
        assert result == Path("output.md")

    def test_get_output_path_default(self):
        """Test get_output_path with default output."""
        input_path = Path("input.docx")
        with patch("src.word_to_md_converter.DEFAULT_OUTPUT_FOLDER", Path("md")):
            result = get_output_path(input_path, None)
            assert result == Path("md/input.md")

    @patch("pypandoc.get_pandoc_path")
    def test_check_pandoc_installation_success(self, mock_get_path):
        """Test check_pandoc_installation when Pandoc is available."""
        mock_get_path.return_value = "/usr/bin/pandoc"
        # Should not raise
        check_pandoc_installation()

    @patch("pypandoc.get_pandoc_path")
    def test_check_pandoc_installation_failure(self, mock_get_path):
        """Test check_pandoc_installation when Pandoc is not available."""
        mock_get_path.return_value = None
        with pytest.raises(SystemExit):
            check_pandoc_installation()
