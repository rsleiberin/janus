import numpy as np
import matplotlib.pyplot as plt

def generate_sRGB_graph(output_path="sRGB_vs_Linearized.png"):
    """
    Generates a graph comparing the sRGB gamma curve and the linearized light intensity,
    and saves it as a PNG file.

    Parameters:
        output_path (str): Path to save the output image. Default is 'sRGB_vs_Linearized.png'.
    """
    # Create normalized sRGB values (0 to 1)
    xsRGB = np.linspace(0, 1, 500)

    # Define the sRGB gamma correction function
    def sRGB_to_linear(xsRGB):
        linear = np.where(xsRGB <= 0.04045,
                          xsRGB / 12.92,
                          ((xsRGB + 0.055) / 1.055) ** 2.4)
        return linear

    # Apply the linearization function
    linear_values = sRGB_to_linear(xsRGB)

    # Plot the graph
    plt.figure(figsize=(8, 6))
    plt.plot(xsRGB, xsRGB, label='sRGB Perception (Gamma Curve)', linestyle='--', linewidth=2)
    plt.plot(xsRGB, linear_values, label='Linearized Output', linewidth=2)
    plt.title('sRGB Gamma Curve vs Linearized Light Intensity', fontsize=14)
    plt.xlabel('Normalized sRGB Value (Input)', fontsize=12)
    plt.ylabel('Light Intensity (Output)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # Save as PNG
    plt.savefig(output_path, dpi=300)
    print(f"Graph saved as {output_path}")
    plt.show()

if __name__ == "__main__":
    generate_sRGB_graph()
