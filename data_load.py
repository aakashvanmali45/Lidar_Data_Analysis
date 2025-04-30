import numpy as np
import open3d as o3d
import glob
import os

velodyne_path = "2011_09_26/2011_09_26_drive_0001_sync/velodyne_points/data/" # path to velodyne data
bin_files = sorted(glob.glob(os.path.join(velodyne_path, "*.bin")))

print(f"Total Frames: {len(bin_files)}")

for i, file in enumerate(bin_files):

    scan = np.fromfile(file, dtype=np.float32).reshape(-1, 4)
    points = scan[:,:3]

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    intensity = scan[:,3]
    intensity_normalized = (intensity - np.min(intensity) / np.ptp(intensity) + 1e-5)
    colors = np.tile(intensity_normalized.reshape(-1,1),(1,3)) # the tile function copies the intensity value 3 times, first we transpose then [1,3]cpoies it 3 times
    pcd.colors = o3d.utility.Vector3dVector(colors)

    print(f"Showing frame {i+1}/{len(bin_files)}: {os.path.basename(file)}")
    o3d.visualization.draw_geometries([pcd])
    

