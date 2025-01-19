from PIL import Image
from skimage.color import rgb2lab
import numpy as np
import os


def convert_to_lab(input_path, output_path):
    """Convert an image from sRGB to LAB color space."""
    # Load the image
    img = Image.open(input_path).convert("RGB")
    img_array = np.array(img)  # Convert to numpy array

    # Convert to LAB color space
    lab_array = rgb2lab(img_array)

    # Save LAB values to a .npy file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.save(output_path, lab_array)
    print(f"LAB data saved to {output_path}")


if __name__ == "__main__":
    input_image = "data/images/example.png"
    output_file = "../data/intermediate/example_lab.npy"
    convert_to_lab(input_image, output_file)
