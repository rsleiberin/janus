import matplotlib.pyplot as plt
import numpy as np
import re

# File path for the input data
input_file = "color_data_lab.txt"

# Luminosity layer boundaries
hardware_boundary = 0.006048833023
first_layer_lower = 0.006048833023
second_layer_lower = 0.1181464
third_layer_lower = 0.458615284
second_layer_upper = 0.3
first_layer_upper = 0.0653794236

# Initialize a list to store luminosity values
luminosity_values = []

def parse_luminosity_data(file_path):
    """Parses the color_data_lab.txt file and extracts luminosity (L) values."""
    line_number = 0  # Track line numbers for debugging
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line_number += 1

                # Skip the header or empty lines
                if line.startswith("sRGB Color") or not line.strip():
                    continue

                try:
                    # Split the line using regex to handle various cases
                    parts = re.split(r',\s*(?![^()]*\))', line.strip())

                    # Extract LAB values enclosed in parentheses after "LAB Color"
                    lab_part = next((part for part in parts if part.startswith('(') and ')' in part and '.' in part), None)
                    if lab_part is None:
                        raise ValueError("LAB values not found")

                    lab_values = lab_part.strip()[1:-1]  # Remove parentheses
                    lab_components = lab_values.split(',')

                    if len(lab_components) != 3:
                        raise ValueError("Incomplete LAB values")

                    # Extract and clean each component of LAB
                    l_value = float(lab_components[0].strip())
                    luminosity_values.append(l_value)
                except Exception as e:
                    print(f"Error parsing line {line_number}: {line.strip()} - {e}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

    return luminosity_values

def plot_luminosity_chart(luminosity_values):
    """Plots the luminosity distribution with layer boundaries and saves the chart as an image."""
    # Create bins for luminosity values
    bins = np.linspace(0, 100, 1000)

    # Count luminosity values within each bin
    counts, bin_edges = np.histogram(luminosity_values, bins=bins)

    # Plot the histogram
    plt.figure(figsize=(10, 8))
    plt.barh(bin_edges[:-1], counts, height=np.diff(bin_edges), color="gray", edgecolor="black")

    # Add color-filled zones
    plt.axhspan(0, first_layer_lower * 100, color='red', alpha=0.3, label="Hardware Boundary")  # Hardware Boundary
    plt.axhspan(first_layer_lower * 100, first_layer_upper * 100, color='blue', alpha=0.3, label="Background Zone")  # Background Zone
    plt.axhspan(second_layer_lower * 100, second_layer_upper * 100, color='green', alpha=0.3, label="Card Zone")  # Card Zone
    plt.axhspan(third_layer_lower * 100, 100, color='yellow', alpha=0.3, label="Action Zone")  # Action Zone

    # Add layer boundaries
    plt.axhline(y=hardware_boundary * 100, color='red', linestyle='--', label="Hardware Boundary Line")
    plt.axhline(y=first_layer_lower * 100, color='blue', linestyle='--', label="First Layer Lower Boundary")
    plt.axhline(y=first_layer_upper * 100, color='cyan', linestyle='--', label="First Layer Upper Boundary")
    plt.axhline(y=second_layer_lower * 100, color='green', linestyle='--', label="Second Layer Lower Boundary")
    plt.axhline(y=second_layer_upper * 100, color='lime', linestyle='--', label="Second Layer Upper Boundary")
    plt.axhline(y=third_layer_lower * 100, color='purple', linestyle='--', label="Third Layer Lower Boundary")

    # Add labels and legend
    plt.xlabel("Count")
    plt.ylabel("Luminosity (L)")
    plt.title("Luminosity Layer Distribution with Zones")
    plt.legend()

    # Save the chart as an image
    plt.savefig("luminosity_layer_zones.png")
    print("Luminosity layer distribution chart with zones saved as luminosity_layer_zones.png")

# Main program execution
if __name__ == "__main__":
    luminosity_values = parse_luminosity_data(input_file)
    if luminosity_values:
        plot_luminosity_chart(luminosity_values)
