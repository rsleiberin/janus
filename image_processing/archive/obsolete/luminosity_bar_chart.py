import numpy as np
import matplotlib.pyplot as plt
import re


def load_luminosity_data(file_path):
    luminosities = []
    try:
        with open(file_path, "r") as file:
            header = next(file)  # Skip the header
            print(f"Header: {header.strip()}")
            for line in file:
                if line.strip():
                    try:
                        parts = re.findall(r"\((.*?)\)", line)
                        if len(parts) >= 2:
                            lab_str = parts[1]
                            l = float(lab_str.split(",")[0])
                            luminosities.append(l)
                        else:
                            print(f"Skipping malformed line: {line.strip()}")
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing line: {line.strip()}")
                        print(f"Exception: {e}")
        print(f"Loaded {len(luminosities)} luminosity values.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return np.array(luminosities)


def plot_luminosity_distribution(
    luminosities, bin_size=0.1, output_file="luminosity_distribution.png"
):
    if len(luminosities) == 0:
        print("No luminosity data to plot.")
        return

    # Create bins from 0 to 100 with 0.1 increments
    bins = np.arange(0, 100 + bin_size, bin_size)
    counts, bin_edges = np.histogram(luminosities, bins=bins)

    # Reverse the bins and counts to match the desired Y-axis orientation (100 at the top)
    bin_edges = bin_edges[::-1]
    counts = counts[::-1]

    plt.figure(figsize=(10, 12))
    plt.barh(
        bin_edges[:-1], counts, height=bin_size, color="skyblue", edgecolor="black"
    )
    plt.xlabel("Count")
    plt.ylabel("Luminosity (L)")
    plt.title("Distribution of Luminosity (L) Values")
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    # Label each bar with the count if the count is significant
    for i, count in enumerate(counts):
        if count > 0:
            plt.text(
                count, bin_edges[i] + bin_size / 2, str(count), va="center", fontsize=6
            )

    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Saved chart to {output_file}")


if __name__ == "__main__":
    input_path = "clustered_lab_data.txt"
    luminosities = load_luminosity_data(input_path)
    if len(luminosities) > 0:
        plot_luminosity_distribution(
            luminosities, bin_size=0.1, output_file="luminosity_distribution.png"
        )
    else:
        print("No valid luminosity data found.")
