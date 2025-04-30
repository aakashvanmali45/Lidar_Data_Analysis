import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import glob
import os

velodyne_dir = "2011_09_26/2011_09_26_drive_0001_sync/velodyne_points/data/" # path to velodyne data
output_dir = "preprocessed_pcd/"
os.makedirs(output_dir, exist_ok=True)

voxel_size = 0.2
outlier_nb_neighbors = 20
outlier_std_ratio = 2.0
ground_dist_thresh = 0.2
dbscan_eps = 0.5  # Max distance between points in a cluster (meters)
dbscan_min_points = 10

bin_files = sorted(glob.glob(os.path.join(velodyne_dir, "*.bin")))
print(f" Processing {len(bin_files)} Lidar frames")

for i, file in enumerate(bin_files):
    
    scans = np.fromfile(file, dtype=np.float32).reshape(-1, 4)
    points = scans[:,:3]

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    pcd = pcd.voxel_down_sample(voxel_size=voxel_size)

    pcd, ind = pcd.remove_statistical_outlier(nb_neighbors=outlier_nb_neighbors, std_ratio=outlier_std_ratio)

    try:
        plane_model, inliers = pcd.segment_plane(distance_threshold=ground_dist_thresh, ransac_n=3, num_iterations=1000)

        pcd_objects = pcd.select_by_index(inliers, invert = True)

    except:
        pcd_objects = pcd

    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Error) as cm:
        labels = np.array(pcd_objects.cluster_dbscan(eps=dbscan_eps,
                                                     min_points=dbscan_min_points,
                                                     print_progress=False))

    max_label = labels.max()
    print(f"[{i+1}/{len(bin_files)}] Found {max_label + 1} object clusters")

    colors = plt.get_cmap("tab20")(labels / (max_label + 1 if max_label >= 0 else 1))
    colors[labels < 0] = 0  # Noise = black
    pcd_objects.colors = o3d.utility.Vector3dVector(colors[:, :3])

    # Save processed point cloud
    filename = os.path.join(output_dir, f"frame_{i:04d}.pcd")
    o3d.io.write_point_cloud(filename, pcd_objects)

    # Optional: Display one frame
    if i == 0:
        o3d.visualization.draw_geometries([pcd_objects], window_name="Segmented Clusters")

print(f"\n✅ All processed point clouds saved in: {output_dir}")
