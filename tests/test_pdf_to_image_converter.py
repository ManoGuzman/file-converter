# tests/test_pdf_to_image_converter.py
"""
Unit tests for the pdf_to_image_converter module.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from src.pdf_to_image_converter import (
    convert_pdf_to_images,
    process_pdfs,
    get_pdf_files_from_folder,
)


def _create_mock_image(size=(100, 100), color="red"):
    """Helper to create a mock PIL Image."""
    return Image.new("RGB", size, color)


class TestConvertPdfToImages:
    """Test class for the convert_pdf_to_images function."""

    @patch("src.pdf_to_image_converter.convert_from_path")
    def test_successful_conversion(self, mock_convert):
        """Test that a valid PDF is converted to images."""
        mock_convert.return_value = [_create_mock_image(), _create_mock_image()]
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = os.path.join(tmp_dir, "test.pdf")
            Path(pdf_path).write_bytes(b"fake pdf")

            convert_pdf_to_images(pdf_path, tmp_dir)

            assert os.path.exists(os.path.join(tmp_dir, "test_page_1.png"))
            assert os.path.exists(os.path.join(tmp_dir, "test_page_2.png"))

    @patch("src.pdf_to_image_converter.convert_from_path")
    def test_single_page_pdf(self, mock_convert):
        """Test conversion of a single-page PDF."""
        mock_convert.return_value = [_create_mock_image()]
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = os.path.join(tmp_dir, "single.pdf")
            Path(pdf_path).write_bytes(b"fake pdf")

            convert_pdf_to_images(pdf_path, tmp_dir)

            assert os.path.exists(os.path.join(tmp_dir, "single_page_1.png"))

    @patch("src.pdf_to_image_converter.convert_from_path")
    def test_output_files_are_png(self, mock_convert):
        """Test that output images are saved as PNG."""
        mock_convert.return_value = [_create_mock_image()]
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = os.path.join(tmp_dir, "doc.pdf")
            Path(pdf_path).write_bytes(b"fake pdf")

            convert_pdf_to_images(pdf_path, tmp_dir)

            output_file = os.path.join(tmp_dir, "doc_page_1.png")
            assert output_file.endswith(".png")
            assert os.path.exists(output_file)

    @patch("src.pdf_to_image_converter.convert_from_path")
    def test_file_not_found_error(self, mock_convert):
        """Test handling of FileNotFoundError."""
        mock_convert.side_effect = FileNotFoundError("File not found")
        with tempfile.TemporaryDirectory() as tmp_dir:
            convert_pdf_to_images("/nonexistent/file.pdf", tmp_dir)
            # Should not raise, just print error
            assert len(os.listdir(tmp_dir)) == 0

    @patch("src.pdf_to_image_converter.convert_from_path")
    def test_os_error(self, mock_convert):
        """Test handling of OSError."""
        mock_convert.side_effect = OSError("Disk error")
        with tempfile.TemporaryDirectory() as tmp_dir:
            convert_pdf_to_images("some.pdf", tmp_dir)
            assert len(os.listdir(tmp_dir)) == 0

    @patch("src.pdf_to_image_converter.convert_from_path")
    def test_value_error(self, mock_convert):
        """Test handling of ValueError."""
        mock_convert.side_effect = ValueError("Invalid value")
        with tempfile.TemporaryDirectory() as tmp_dir:
            convert_pdf_to_images("some.pdf", tmp_dir)
            assert len(os.listdir(tmp_dir)) == 0

    @patch("src.pdf_to_image_converter.convert_from_path")
    def test_page_naming_convention(self, mock_convert):
        """Test that pages are named with correct convention: basename_page_N.png."""
        mock_convert.return_value = [
            _create_mock_image(),
            _create_mock_image(),
            _create_mock_image(),
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = os.path.join(tmp_dir, "report.pdf")
            Path(pdf_path).write_bytes(b"fake pdf")

            convert_pdf_to_images(pdf_path, tmp_dir)

            for i in range(1, 4):
                expected = os.path.join(tmp_dir, f"report_page_{i}.png")
                assert os.path.exists(expected)


class TestProcessPdfs:
    """Test class for the process_pdfs function."""

    @patch("src.pdf_to_image_converter.convert_from_path")
    def test_process_multiple_pdfs(self, mock_convert):
        """Test processing a list of multiple PDFs."""
        mock_convert.return_value = [_create_mock_image()]
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_paths = []
            for name in ["a.pdf", "b.pdf"]:
                pdf_path = os.path.join(tmp_dir, name)
                Path(pdf_path).write_bytes(b"fake pdf")
                pdf_paths.append(pdf_path)

            process_pdfs(pdf_paths, tmp_dir)

            assert os.path.exists(os.path.join(tmp_dir, "a_page_1.png"))
            assert os.path.exists(os.path.join(tmp_dir, "b_page_1.png"))

    @patch("src.pdf_to_image_converter.convert_from_path")
    def test_process_empty_list(self, mock_convert):
        """Test processing an empty list of PDFs."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            process_pdfs([], tmp_dir)
            mock_convert.assert_not_called()


class TestGetPdfFilesFromFolder:
    """Test class for the get_pdf_files_from_folder function."""

    def test_folder_with_pdfs(self):
        """Test that PDF files in a folder are returned."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf1 = os.path.join(tmp_dir, "doc1.pdf")
            pdf2 = os.path.join(tmp_dir, "doc2.pdf")
            Path(pdf1).write_bytes(b"fake")
            Path(pdf2).write_bytes(b"fake")

            result = get_pdf_files_from_folder(tmp_dir)
            assert len(result) == 2
            assert all(p.endswith(".pdf") for p in result)

    def test_folder_without_pdfs(self):
        """Test that a folder with no PDFs returns an empty list."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            txt_path = os.path.join(tmp_dir, "notes.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("hello")

            result = get_pdf_files_from_folder(tmp_dir)
            assert result == []

    def test_empty_folder(self):
        """Test that an empty folder returns an empty list."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = get_pdf_files_from_folder(tmp_dir)
            assert result == []

    def test_mixed_files(self):
        """Test that only PDF files are returned from a mixed folder."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = os.path.join(tmp_dir, "report.pdf")
            txt_path = os.path.join(tmp_dir, "notes.txt")
            img_path = os.path.join(tmp_dir, "photo.png")
            Path(pdf_path).write_bytes(b"fake")
            Path(txt_path).write_text("hello", encoding="utf-8")
            Path(img_path).write_bytes(b"fake")

            result = get_pdf_files_from_folder(tmp_dir)
            assert len(result) == 1
            assert result[0].endswith(".pdf")

    def test_ignores_subdirectories_named_pdf(self):
        """Test that subdirectories ending in .pdf are not included."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            fake_dir = os.path.join(tmp_dir, "folder.pdf")
            os.makedirs(fake_dir)

            result = get_pdf_files_from_folder(tmp_dir)
            assert result == []

    def test_case_insensitive_extension(self):
        """Test that .PDF (uppercase) files are also found."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = os.path.join(tmp_dir, "REPORT.PDF")
            Path(pdf_path).write_bytes(b"fake")

            result = get_pdf_files_from_folder(tmp_dir)
            assert len(result) == 1
