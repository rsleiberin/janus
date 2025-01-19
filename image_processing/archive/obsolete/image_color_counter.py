from PIL import Image
from collections import defaultdict
import argparse
import os


def process_image(image_path):
    # Open the image and convert it to RGB
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        width, height = img.size

        # Dictionary to store color counts
        color_count = defaultdict(int)

        # Iterate through each pixel and count colors
        for x in range(width):
            for y in range(height):
                pixel = img.getpixel((x, y))
                color_count[pixel] += 1

        return color_count


def save_results(color_count, output_file):
    with open(output_file, "w") as f:
        f.write("sRGB Color (R, G, B), Count\n")
        for color, count in sorted(color_count.items()):
            f.write(f"{color}, {count}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Count unique colors in an image and save as sRGB data with counts."
    )
    parser.add_argument("image_path", help="Path to the image file (PNG or JPEG).")
    parser.add_argument("output_file", help="Output file to save the color data.")
    args = parser.parse_args()

    if not os.path.isfile(args.image_path):
        print(f"Error: File '{args.image_path}' not found.")
        return

    color_count = process_image(args.image_path)
    save_results(color_count, args.output_file)
    print(f"Color data has been saved to '{args.output_file}'.")


if __name__ == "__main__":
    main()
