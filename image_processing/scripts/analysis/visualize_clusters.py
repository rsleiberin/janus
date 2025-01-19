import numpy as np
import matplotlib.pyplot as plt
import os


def visualize_clusters(cluster_path, output_path):
    """Visualize cluster labels as an image."""
    # Load cluster labels
    cluster_labels = np.load(cluster_path)

    # Generate a plot
    plt.figure(figsize=(8, 8))
    plt.imshow(cluster_labels, cmap="tab20")  # Use a color map
    plt.axis("off")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    print(f"Cluster visualization saved to {output_path}")


if __name__ == "__main__":
    cluster_file = "../data/results/example_clusters.npy"
    output_image = "../data/results/example_clusters.png"
    visualize_clusters(cluster_file, output_image)
