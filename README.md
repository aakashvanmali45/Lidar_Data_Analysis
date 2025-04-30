# LIDAR Data Analysis and 3D Object Tracking using Python + Open3D

This project implements an end-to-end pipeline for analyzing LIDAR sensor data, segmenting 3D objects using clustering, and tracking them across frames using a centroid-based tracker.

## Dataset
- **KITTI Vision Benchmark** (raw velodyne point clouds) [Link to download](https://www.cvlibs.net/datasets/kitti/raw_data.php)


## Project Pipeline
1. **LIDAR Data Loading** (`.bin` → numpy array)
2. **Preprocessing**: Outlier removal, range filtering
3. **Clustering**: DBSCAN for object segmentation
4. **Bounding Boxes**: Axis-Aligned 3D boxes
5. **Tracking**: Centroid-based multi-object tracking
6. **Visualization**: Animated Open3D viewer & video export

## Technologies Used
- `Python`
- `Open3D`
- `NumPy`, `SciPy`, `Matplotlib`
- `DBSCAN` from `scikit-learn`

## Demo

![Demo](tracking_output.avi)



## How to run the project
1. Download the data from the above link.
2. 



## 🧠 Skills Highlighted
- Robotics Perception
- LIDAR Sensor Data Handling
- Point Cloud Denoising & Clustering
- 3D Object Detection & Tracking
- Real-time 3D Visualization
