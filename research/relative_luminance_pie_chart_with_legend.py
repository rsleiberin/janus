import matplotlib.pyplot as plt

# Data for relative luminance
labels = ['Red', 'Green', 'Blue']
luminance_values = [0.2126, 0.7152, 0.0722]

# Colors for the pie chart
colors = ['#FF5733', '#33FF57', '#3357FF']

# Create the pie chart
plt.figure(figsize=(8, 6))
wedges, texts, autotexts = plt.pie(
    luminance_values, labels=labels, autopct='%1.1f%%',
    colors=colors, startangle=140, textprops=dict(color="w")
)

# Add a legend with exact luminance values
plt.legend(
    loc="best",
    labels=[f"{label}: {value:.4f}" for label, value in zip(labels, luminance_values)],
    title="Relative Luminance Values"
)

# Title and layout adjustments
plt.title('Relative Luminance Contributions')
plt.tight_layout()

# Save the pie chart as PNG
output_path = "relative_luminance_pie_chart_with_legend.png"
plt.savefig(output_path, dpi=300)
print(f"Pie chart saved as {output_path}")
plt.show()
