# tests/test_image_to_pdf_converter.py
"""
Unit tests for the image_to_pdf_converter module.
"""

import os
import tempfile
from pathlib import Path

import pytest
from PIL import Image

from src.image_to_pdf_converter import get_image_paths, convert_images_to_pdf


def _create_test_image(path, size=(100, 100), color="red"):
    """Helper to create a simple test image."""
    img = Image.new("RGB", size, color)
    img.save(path)


class TestGetImagePaths:
    """Test class for the get_image_paths function."""

    def test_single_image_file(self):
        """Test that a single valid image file returns its path."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
            _create_test_image(tmp_path)
        try:
            result = get_image_paths(tmp_path)
            assert result == [tmp_path]
        finally:
            os.unlink(tmp_path)

    def test_single_non_image_file(self):
        """Test that a non-image file returns an empty list."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"not an image")
            tmp_path = tmp.name
        try:
            result = get_image_paths(tmp_path)
            assert result == []
        finally:
            os.unlink(tmp_path)

    def test_folder_with_images(self):
        """Test that a folder with images returns all image paths."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            extensions = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]
            expected = []
            for ext in extensions:
                img_path = os.path.join(tmp_dir, f"test{ext}")
                _create_test_image(img_path)
                expected.append(img_path)

            result = get_image_paths(tmp_dir)
            assert sorted(result) == sorted(expected)

    def test_folder_with_mixed_files(self):
        """Test that a folder with mixed files only returns image paths."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            img_path = os.path.join(tmp_dir, "image.png")
            _create_test_image(img_path)
            txt_path = os.path.join(tmp_dir, "notes.txt")
            Path(txt_path).write_text("hello", encoding="utf-8")

            result = get_image_paths(tmp_dir)
            assert result == [img_path]

    def test_empty_folder(self):
        """Test that an empty folder returns an empty list."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = get_image_paths(tmp_dir)
            assert result == []

    def test_nonexistent_path(self):
        """Test that a non-existent path returns an empty list."""
        result = get_image_paths("/nonexistent/path")
        assert result == []

    @pytest.mark.parametrize("ext", [".png", ".jpg", ".jpeg", ".bmp", ".gif"])
    def test_supported_extensions(self, ext):
        """Test that each supported image extension is recognized."""
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp_path = tmp.name
            _create_test_image(tmp_path)
        try:
            result = get_image_paths(tmp_path)
            assert result == [tmp_path]
        finally:
            os.unlink(tmp_path)


class TestConvertImagesToPdf:
    """Test class for the convert_images_to_pdf function."""

    def test_single_image_to_pdf(self):
        """Test converting a single image to PDF."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            img_path = os.path.join(tmp_dir, "test.png")
            _create_test_image(img_path)
            out_pdf = os.path.join(tmp_dir, "output.pdf")

            convert_images_to_pdf([img_path], out_pdf)

            assert os.path.exists(out_pdf)
            assert os.path.getsize(out_pdf) > 0

    def test_multiple_images_to_pdf(self):
        """Test converting multiple images into a single PDF."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            img_paths = []
            for i in range(3):
                img_path = os.path.join(tmp_dir, f"test_{i}.png")
                _create_test_image(img_path, color=["red", "green", "blue"][i])
                img_paths.append(img_path)
            out_pdf = os.path.join(tmp_dir, "output.pdf")

            convert_images_to_pdf(img_paths, out_pdf)

            assert os.path.exists(out_pdf)
            assert os.path.getsize(out_pdf) > 0

    def test_empty_list_no_pdf_created(self):
        """Test that an empty image list does not create a PDF."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_pdf = os.path.join(tmp_dir, "output.pdf")

            convert_images_to_pdf([], out_pdf)

            assert not os.path.exists(out_pdf)

    def test_invalid_image_skipped(self):
        """Test that invalid image files are skipped without crashing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            invalid_path = os.path.join(tmp_dir, "bad.png")
            Path(invalid_path).write_text("not a real image", encoding="utf-8")
            valid_path = os.path.join(tmp_dir, "good.png")
            _create_test_image(valid_path)
            out_pdf = os.path.join(tmp_dir, "output.pdf")

            convert_images_to_pdf([invalid_path, valid_path], out_pdf)

            assert os.path.exists(out_pdf)

    def test_all_invalid_images_no_pdf(self):
        """Test that only invalid images results in no PDF."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            invalid_path = os.path.join(tmp_dir, "bad.png")
            Path(invalid_path).write_text("not a real image", encoding="utf-8")
            out_pdf = os.path.join(tmp_dir, "output.pdf")

            convert_images_to_pdf([invalid_path], out_pdf)

            assert not os.path.exists(out_pdf)

    def test_different_image_formats(self):
        """Test converting images of different formats into a PDF."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            img_paths = []
            for ext in [".png", ".jpg", ".bmp"]:
                img_path = os.path.join(tmp_dir, f"test{ext}")
                _create_test_image(img_path)
                img_paths.append(img_path)
            out_pdf = os.path.join(tmp_dir, "output.pdf")

            convert_images_to_pdf(img_paths, out_pdf)

            assert os.path.exists(out_pdf)
            assert os.path.getsize(out_pdf) > 0
