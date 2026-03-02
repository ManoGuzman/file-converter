"""
Image to PDF Converter Script.
"""

import os
import argparse
from PIL import Image, UnidentifiedImageError

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


# Function to get image paths from a file or folder
def get_image_paths(path):
    """Return a list of image file paths from the given file or folder."""
    if os.path.isfile(path):
        if path.lower().endswith(IMAGE_EXTENSIONS):
            return [path]
        else:
            return []
    elif os.path.isdir(path):
        return [
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.lower().endswith(IMAGE_EXTENSIONS)
        ]
    else:
        return []


# Function to convert images to PDF
def convert_images_to_pdf(images_list, out_pdf):
    """
    Converts all images in the list to a single PDF.
    """
    images = []
    for img_path in images_list:
        try:
            img = Image.open(img_path).convert("RGB")
            images.append(img)
        except UnidentifiedImageError:
            print(f"Warning: {img_path} is not a valid image and will be skipped.")
    if images:
        images[0].save(out_pdf, save_all=True, append_images=images[1:])
    else:
        print("No valid images found.")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    default_input = os.path.join(parent_dir, "img")
    output_folder = os.path.join(parent_dir, "pdf")
    os.makedirs(output_folder, exist_ok=True)

    parser = argparse.ArgumentParser(description="Image to PDF Converter")
    parser.add_argument("-f", "--file", help="Path to individual image file or folder")
    args = parser.parse_args()

    input_path = args.file if args.file else default_input
    image_paths = get_image_paths(input_path)

    # Determine output PDF name
    if args.file and os.path.isfile(args.file):
        filename = os.path.splitext(os.path.basename(args.file))[0] + ".pdf"
        output_pdf = os.path.join(output_folder, filename)
    else:
        output_pdf = os.path.join(output_folder, "output.pdf")

    convert_images_to_pdf(image_paths, output_pdf)
