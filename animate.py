import open3d as o3d
import time
import glob
import os

pcd_dir = "preprocessed_pcd/"
pcd_files = sorted(glob.glob(os.path.join(pcd_dir, "*.pcd")))


vis = o3d.visualization.Visualizer()
vis.create_window(window_name='LIDAR Animation', width=1024, height=768)
geom_added = False

for i, file in enumerate(pcd_files):
    print(f"Loading: {file}")
    pcd = o3d.io.read_point_cloud(file)

    if not pcd.has_points():
        print(f"Warning: {file} has no points.")
        continue

    if not geom_added:
        vis.add_geometry(pcd)
        geom_added = True
    else:
        vis.clear_geometries()
        vis.add_geometry(pcd)

    vis.poll_events()
    vis.update_renderer()
    vis.get_view_control().set_zoom(0.5)  # Adjust zoom if needed
    time.sleep(0.1)  # Adjust for playback speed

vis.destroy_window()
