"""
Image to PDF Converter Script.
"""

import os
from PIL import Image, UnidentifiedImageError

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


# Function to get image files from a folder
def get_image_files(folder):
    """Return a list of image files in the given folder."""
    return [f for f in os.listdir(folder) if f.lower().endswith(IMAGE_EXTENSIONS)]


# Function to convert images to PDF
def convert_images_to_pdf(img_folder, out_pdf):
    """
    Converts all images in a folder to a single PDF.
    """
    image_files = get_image_files(img_folder)
    images = []
    for file in image_files:
        img_path = os.path.join(img_folder, file)
        try:
            img = Image.open(img_path).convert("RGB")
            images.append(img)
        except UnidentifiedImageError:
            print(f"Warning: {file} is not a valid image and will be skipped.")
    if images:
        images[0].save(out_pdf, save_all=True, append_images=images[1:])
    else:
        print("No valid images found in the folder.")


if __name__ == "__main__":
    # Example usage
    IMAGE_FOLDER = "img"  # Folder containing images
    OUTPUT_PDF = "output.pdf"  # Output PDF file name
    convert_images_to_pdf(IMAGE_FOLDER, OUTPUT_PDF)
