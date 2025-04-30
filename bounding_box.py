import open3d as o3d
import numpy as np
import glob
import os
import json
from sklearn.cluster import DBSCAN

# Paths
pcd_dir = "preprocessed_pcd/"
bbox_label_dir = "bbox_labels/"
os.makedirs(bbox_label_dir, exist_ok=True)

# DBSCAN parameters
eps = 0.8  # max distance between points in a cluster (meters)
min_samples = 10  # minimum number of points per cluster

pcd_files = sorted(glob.glob(os.path.join(pcd_dir, "*.pcd")))

for frame_id, file in enumerate(pcd_files):
    pcd = o3d.io.read_point_cloud(file)
    points = np.asarray(pcd.points)

    
    if len(points) == 0:
        continue

    
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    labels = clustering.labels_
    unique_labels = np.unique(labels)

    bboxes = []
    for label in unique_labels:
        if label == -1:
            continue  

        cluster_points = points[labels == label]
        if len(cluster_points) < 10:
            continue

        cluster_pcd = o3d.geometry.PointCloud()
        cluster_pcd.points = o3d.utility.Vector3dVector(cluster_points)

        
        aabb = cluster_pcd.get_axis_aligned_bounding_box()
        bbox = {
            "min_bound": aabb.get_min_bound().tolist(),
            "max_bound": aabb.get_max_bound().tolist(),
            "label": "vehicle",  # Placeholder label
            "id": int(label)
        }
        bboxes.append(bbox)

    
    with open(f"{bbox_label_dir}/frame_{frame_id:04d}.json", "w") as f:
        json.dump(bboxes, f, indent=2)

    print(f"Frame {frame_id}: saved {len(bboxes)} bounding boxes.")
