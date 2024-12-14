import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_clustered_lab_data(file_path):
    lab_data = []
    labels = []
    with open(file_path, 'r') as file:
        next(file)  # Skip the header
        for line in file:
            if line.strip():
                try:
                    parts = line.strip().split(',')
                    l, a, b = map(float, parts[:3])
                    cluster = int(parts[3])
                    lab_data.append([l, a, b])
                    labels.append(cluster)
                except ValueError as e:
                    print(f"Error parsing line: {line}")
                    print(f"Exception: {e}")
    return np.array(lab_data), np.array(labels)

def visualize_lab_data(lab_data, labels):
    if len(lab_data) == 0:
        print("No data to visualize.")
        return

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    unique_labels = set(labels)

    print(f"Unique clusters found: {unique_labels}")

    for label in unique_labels:
        clustered_points = lab_data[labels == label]
        if len(clustered_points) > 0:
            ax.scatter(clustered_points[:, 0], clustered_points[:, 1], clustered_points[:, 2], label=f'Cluster {label}')

    ax.set_xlabel('L')
    ax.set_ylabel('A')
    ax.set_zlabel('B')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    input_path = "clustered_lab_data.txt"
    try:
        lab_data, labels = load_clustered_lab_data(input_path)
        print(f"Loaded {len(lab_data)} data points.")
        visualize_lab_data(lab_data, labels)
    except FileNotFoundError:
        print(f"File not found: {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
