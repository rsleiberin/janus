import numpy as np
from sklearn.cluster import DBSCAN
import re

def load_lab_data(file_path):
    lab_data = []
    sRGB_data = []
    counts = []
    with open(file_path, 'r') as file:
        next(file)  # Skip the header
        for line in file:
            if line.strip():
                try:
                    parts = re.findall(r"\((.*?)\)", line)
                    rgb_str = parts[0]
                    lab_str = parts[1]
                    count = int(line.split(",")[1].strip())

                    r, g, b = map(int, rgb_str.split(","))
                    l, a, b_ = map(float, lab_str.split(","))

                    sRGB_data.append((r, g, b))
                    lab_data.append([l, a, b_])
                    counts.append(count)
                except (ValueError, IndexError) as e:
                    print(f"Error parsing line: {line}")
                    print(f"Exception: {e}")

    return np.array(lab_data), sRGB_data, counts

def cluster_colors(lab_data, eps=2.5, min_samples=2):
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(lab_data)
    return labels

def save_clustered_data(sRGB_data, counts, lab_data, labels, output_path):
    unique_labels = set(labels)
    total_groups = len(unique_labels - {-1})  # Exclude noise cluster (-1)

    with open(output_path, 'w') as file:
        file.write(f"sRGB Color (R, G, B), Count, LAB Color (L, A, B), Group Number (Total Groups: {total_groups})\n")
        for (rgb, count, lab, label) in zip(sRGB_data, counts, lab_data, labels):
            file.write(f"({rgb[0]}, {rgb[1]}, {rgb[2]}), {count}, ({lab[0]:.2f}, {lab[1]:.2f}, {lab[2]:.2f}), {label}\n")
    
    print(f"Saved clustered data with {total_groups} groups to {output_path}")

def find_group_colors(sRGB_data, counts, labels):
    unique_labels = set(labels) - {-1}  # Exclude noise
    group_colors = {}

    for label in unique_labels:
        indices = [i for i, lbl in enumerate(labels) if lbl == label]
        max_count_index = max(indices, key=lambda i: counts[i])
        group_colors[label] = sRGB_data[max_count_index]

    return group_colors

def save_group_colors(group_colors, output_path):
    with open(output_path, 'w') as file:
        file.write("Group Number, Group Color (R, G, B)\n")
        for label, color in group_colors.items():
            file.write(f"{label}, ({color[0]}, {color[1]}, {color[2]})\n")

    print(f"Saved group colors to {output_path}")

if __name__ == "__main__":
    input_path = "color_data_lab.txt"
    clustered_output_path = "clustered_lab_data.txt"
    group_colors_output_path = "group_colors.txt"

    lab_data, sRGB_data, counts = load_lab_data(input_path)
    if lab_data.size > 0:
        labels = cluster_colors(lab_data, eps=2.5, min_samples=2)
        save_clustered_data(sRGB_data, counts, lab_data, labels, clustered_output_path)
        group_colors = find_group_colors(sRGB_data, counts, labels)
        save_group_colors(group_colors, group_colors_output_path)
    else:
        print("No valid LAB data found in the file.")
