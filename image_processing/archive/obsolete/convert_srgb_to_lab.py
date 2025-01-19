import colorspacious as cs
import ast
import re


def srgb_to_lab(rgb):
    # Normalize sRGB values to the range [0, 1]
    r, g, b = rgb
    normalized_rgb = (r / 255, g / 255, b / 255)
    lab = cs.cspace_convert(normalized_rgb, start={"name": "sRGB1"}, end="CIELab")
    return lab


def process_color_data(input_file, output_file):
    with open(input_file, "r") as infile:
        lines = infile.readlines()

    # Prepare output file
    with open(output_file, "w") as outfile:
        outfile.write("sRGB Color (R, G, B), Count, LAB Color (L, A, B)\n")

        # Skip the header line
        for line in lines[1:]:
            match = re.match(r"\((\d+), (\d+), (\d+)\), (\d+)", line.strip())
            if match:
                r, g, b, count = map(int, match.groups())
                lab = srgb_to_lab((r, g, b))
                outfile.write(
                    f"({r}, {g}, {b}), {count}, ({lab[0]:.2f}, {lab[1]:.2f}, {lab[2]:.2f})\n"
                )


def main():
    input_file = "color_data.txt"
    output_file = "color_data_lab.txt"
    process_color_data(input_file, output_file)
    print(f"Conversion complete. LAB data saved to '{output_file}'.")


if __name__ == "__main__":
    main()
