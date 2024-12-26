# Image Processing Directory

## Overview
This directory is part of the exploratory phase of the design system, focusing on research and prototyping image processing techniques for clustering, visualizing, and deriving information from images. The insights gathered here are foundational to the design system and its components.

## Goals
1. **Extract Image Data:**
   - Capture LAB, RGB, spatial data, and metadata from PNG files.
   - Store data in a scalable database format for future applications.

2. **Perform Clustering and Analysis:**
   - Cluster pixels by color (LAB) and shape (spatial).
   - Generate visualizations to validate clustering and analyze shapes and luminosity.

3. **Prepare for Long-Term Expansion:**
   - Include placeholders for future parameters (e.g., alpha channels).
   - Plan for eventual integration with neural networks and LLMs for advanced applications.

## Directory Structure

image_processing/
├── data/                      # Input images, intermediate files, and results
│   ├── images/                # Raw input images
│   ├── intermediate/          # Temporary files (e.g., LAB arrays)
│   ├── results/               # Final outputs (e.g., clustered images)
├── scripts/                   # Processing and analysis scripts
│   ├── preprocessing/         # Preprocessing and extraction
│   │   ├── extract_metadata.py      # Extracts metadata (dimensions, bit depth, etc.)
│   │   ├── extract_pixels.py        # Extracts pixel data (LAB, RGB, and spatial coordinates)
│   │   ├── extract_alpha.py         # (Future) Extracts alpha channel data for images with transparency
│   ├── analysis/              # Analysis and clustering
│   │   ├── compute_histogram.py     # Computes color histograms for global and regional color distributions
│   │   ├── dbscan_clustering.py     # Performs DBSCAN clustering on LAB and spatial data
│   │   ├── edge_detection.py        # Detects edges in images for shape and feature analysis
│   │   ├── analyze_layers.py        # Analyzes layers and micro-layers based on clustering results
│   │   ├── analyze_alpha.py         # (Future) Processes alpha data for transparency-based analysis
│   ├── storage/               # Storing and managing data
│   │   ├── create_db.py             # Sets up the SQLite database schema
│   │   ├── insert_data.py           # Inserts extracted data into the database
│   │   ├── export_data.py           # Exports data (e.g., JSON or CSV) for external use
│   ├── visualization/         # Visualizations and outputs
│       ├── visualize_clusters.py    # Visualizes DBSCAN clusters
│       ├── visualize_histogram.py   # Visualizes color histograms
│       ├── visualize_shapes.py      # Overlays shape boundaries on original image
│       ├── visualize_layers.py      # Visualizes luminosity layers
├── server/                    # (Future) Server-side API scripts
│   ├── db_api.py                    # API for querying the database
│   ├── image_api.py                 # API for image uploads and retrievals
├── archive/                   # Obsolete or exploratory scripts
├── utils/                     # Helper functions (e.g., file I/O, math operations)
│   ├── file_loader.py               # Loads and validates input image files
├── tests/                     # Test cases for each script
└── README.md                  # This document

## Current Focus
- **Clustering:** Validating DBSCAN using LAB + spatial data.
- **Visualization:** Verifying results through visual analysis.
- **Database Setup:** Structuring scalable data storage for current and future use.

## Future Expansion
- Edge detection, alpha processing, and histograms.
- Integrating derived features into UI design workflows.
- Connecting neural networks and large language models for image descriptions and insights.

# Image Processing Guide

## Overview
This guide provides a detailed walkthrough of the **image_processing** project. It includes the goals, research methodology, database design, modular structure, and implementation stages for each feature. By marking the implementation stage, contributors can understand what has been completed and what is pending.

---

## Goals and Vision
The **image_processing** project is part of the exploratory phase for a design system, focusing on:
1. **Researching Image Data:**
   - Extracting LAB, RGB, spatial data, and metadata from images.
   - Clustering image pixels to uncover relationships between color and spatial patterns.

2. **Informing Luminosity Layers:**
   - Using the results of clustering and shape analysis to define and optimize luminosity layers and micro-layers for UI components.

3. **Future-Ready Scalability:**
   - Preparing the system for integration with agentic neural networks, large language models (LLMs), and alpha channel processing for advanced transparency-based design.

---

## Implementation Stages

- **[✔️ Completed]**: Fully implemented and functional.
- **[🚧 In Progress]**: Currently being developed or partially implemented.
- **[❌ Pending]**: Planned but not yet started.

---

## Walkthrough of the Process

### **1. Preprocessing**
The preprocessing phase ensures that all input data is extracted and formatted consistently for later analysis and visualization.

#### Steps:
1. **Load and Validate Image Data**:
   - Validate input images to ensure they meet required specifications (e.g., PNG format).
   - Extract and store image metadata such as dimensions, bit depth, and compression method.
   - **[✔️ Completed] `extract_metadata.py`**

2. **Extract Pixel Data**:
   - Convert pixels from sRGB to LAB color space.
   - Record spatial information (X, Y coordinates) alongside LAB and RGB values for each pixel.
   - Alpha channels are reserved for future use, with placeholders in the pipeline.
   - **[✔️ Completed] `extract_pixels.py`**
   - **[❌ Pending] `extract_alpha.py`**

3. **Store in Database**:
   - Store metadata, pixel data, and extracted features in a local SQLite database for efficient querying and future scalability.
   - **[🚧 In Progress] `create_db.py`**
   - **[❌ Pending] `insert_data.py`**

---

### **2. Analysis**
The analysis phase focuses on deriving insights from the extracted data.

#### Steps:
1. **Clustering**:
   - Perform DBSCAN clustering on pixel data (LAB values and spatial coordinates).
   - Clustering helps uncover color regions and shapes in the image.
   - **[🚧 In Progress] `dbscan_clustering.py`**

2. **Shape Analysis**:
   - Analyze clusters to identify shapes, bounding boxes, centroids, and areas.
   - This data informs the structure of luminosity layers and micro-layers.
   - **[❌ Pending] `analyze_layers.py`**

3. **Compute Histograms**:
   - Generate color histograms for global and regional analysis of color distribution.
   - **[❌ Pending] `compute_histogram.py`**

4. **Edge Detection**:
   - Detect edges and shapes in the image for further segmentation or feature analysis.
   - **[❌ Pending] `edge_detection.py`**

---

### **3. Storage**
All data extracted and derived during preprocessing and analysis is stored in a **scalable database** for future querying and integration.

#### Database Tables:
1. **Images Table**:
   - Stores metadata about each image, such as filename, dimensions, bit depth, and compression method.
   - **[🚧 In Progress]**

2. **Pixels Table**:
   - Stores pixel-level data, including LAB, RGB, X, Y coordinates, and alpha (when applicable).
   - **[❌ Pending]**

3. **Derived Features Table**:
   - Stores higher-level features such as edge maps, histograms, and bounding boxes.
   - **[❌ Pending]**

#### Scripts:
- `create_db.py`: **[🚧 In Progress]** Sets up the SQLite database schema.
- `insert_data.py`: **[❌ Pending]** Inserts extracted data into the database.
- `export_data.py`: **[❌ Pending]** Exports data in formats suitable for external use (e.g., JSON, CSV).

---

### **4. Visualization**
The visualization phase ensures the results are interpretable and can guide further development.

#### Steps:
1. **Cluster Visualization**:
   - Display clusters generated by DBSCAN to validate the clustering process.
   - **[✔️ Completed] `visualize_clusters.py`**

2. **Shape Visualization**:
   - Overlay clustered shapes on the original image for a better understanding of spatial relationships.
   - **[❌ Pending] `visualize_shapes.py`**

3. **Layer Visualization**:
   - Visualize luminosity layers and their relationship to the image's structure.
   - **[❌ Pending] `visualize_layers.py`**

4. **Histogram Visualization**:
   - Plot histograms to analyze color distributions within the image.
   - **[❌ Pending] `visualize_histogram.py`**

---

### **5. Server Integration**
As the project scales, integration with a backend server will allow for:
1. **Image Uploads**:
   - Enabling users to upload images for processing.
   - **[❌ Pending] `image_api.py`**

2. **Data Querying**:
   - Allowing API calls to query the database for processed results.
   - **[❌ Pending] `db_api.py`**

---

## Best Practices for GitHub Workflow

### **Branching Strategy**
1. Use the **`main`** branch for stable and tested features.
2. Create feature branches for each major implementation:
   - Example: `feature/preprocessing`, `feature/clustering`.
3. Use pull requests to merge branches into `main` after review.

### **Commit Message Guidelines**
- Write clear, concise commit messages with details about the changes:
  - Example: `Add LAB pixel extraction to preprocessing pipeline`.
- Use prefixes to indicate the type of change:
  - `feat`: New feature.
  - `fix`: Bug fix.
  - `refactor`: Code refactoring.
  - `doc`: Documentation updates.

### **Issues and Task Tracking**
- Use GitHub Issues to document bugs, feature requests, and enhancements.
- Break down large tasks into smaller, manageable issues.
- Link pull requests to issues for better traceability.

---

## Why This Project Matters
This project bridges the gap between exploratory image processing and real-world applications:
1. **Research Insight**:
   - Uncover patterns in color and spatial data that inform design.
2. **Scalability**:
   - A robust pipeline ensures that as the project grows, it can handle complex data and integrate new features with ease.
3. **Foundation for UI Design**:
   - The insights gained here are directly applied to building components for the design system.

---

## How to Contribute
1. Follow the directory structure and adhere to modular design principles.
2. Focus on the current research priorities but keep scalability in mind.
3. Use the README and this guide to understand the project's goals and workflows.

---

This guide ensures contributors have a clear understanding of the project, its goals, and the best practices for collaboration. Let me know if you'd like further refinements or additional sections! 🚀
