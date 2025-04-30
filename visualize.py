import open3d as o3d
import numpy as np
import os
import json
import cv2

# Paths
pcd_dir = "preprocessed_pcd/"
tracked_label_dir = "tracked_labels/"
output_video_path = "tracking_output.avi"

# Load files
pcd_files = sorted([f for f in os.listdir(pcd_dir) if f.endswith('.pcd')])
bbox_files = sorted([f for f in os.listdir(tracked_label_dir) if f.endswith('.json')])

# Open3D Visualizer
vis = o3d.visualization.Visualizer()
vis.create_window(width=1280, height=720, visible=False)
render_option = vis.get_render_option()
render_option.background_color = np.array([0, 0, 0])
render_option.point_size = 1.5

# Setup video writer
fps = 10
video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (1280, 720))

for pcd_file, bbox_file in zip(pcd_files, bbox_files):
    vis.clear_geometries()

    # Load point cloud
    pcd = o3d.io.read_point_cloud(os.path.join(pcd_dir, pcd_file))
    vis.add_geometry(pcd)

    # Load bounding boxes
    with open(os.path.join(tracked_label_dir, bbox_file)) as f:
        bboxes = json.load(f)

    # Add AABB bounding boxes
    for bbox in bboxes:
        min_bound = np.array(bbox["min_bound"])
        max_bound = np.array(bbox["max_bound"])
        aabb = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)
        aabb.color = [1, 0, 0]  # Red boxes
        vis.add_geometry(aabb)

    vis.poll_events()
    vis.update_renderer()

    # Capture frame as image
    img = np.asarray(vis.capture_screen_float_buffer(False))
    img = (img * 255).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    video_writer.write(img)
    cv2.imshow('Lidar Tracking', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_writer.release()
vis.destroy_window()
cv2.destroyAllWindows()
print(f"[INFO] Video saved to: {output_video_path}")
