import numpy as np
from sklearn.cluster import DBSCAN
import os

def cluster_lab(input_path, output_path, eps=0.5, min_samples=10):
    """Cluster LAB values using DBSCAN."""
    # Load LAB data
    lab_array = np.load(input_path)
    lab_flat = lab_array.reshape(-1, 3)  # Flatten to 2D array

    # Perform DBSCAN clustering
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(lab_flat)
    labels = clustering.labels_
    
    # Reshape cluster labels to image dimensions
    cluster_labels = labels.reshape(lab_array.shape[:2])
    
    # Save cluster labels
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    np.save(output_path, cluster_labels)
    print(f"Cluster labels saved to {output_path}")

if __name__ == "__main__":
    input_lab = "../data/intermediate/example_lab.npy"
    output_file = "../data/results/example_clusters.npy"
    cluster_lab(input_lab, output_file)
