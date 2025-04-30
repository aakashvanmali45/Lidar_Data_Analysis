import json
import numpy as np
import os
from scipy.spatial.distance import cdist

label_dir = "bbox_labels/"
tracked_output_dir = "tracked_labels/"
os.makedirs(tracked_output_dir, exist_ok=True)

frame_files = sorted([f for f in os.listdir(label_dir) if f.endswith('.json')])

next_track_id = 0
active_tracks = {}  # track_id: centroid

distance_threshold = 2.0  # meters

for frame_num, file in enumerate(frame_files):
    with open(os.path.join(label_dir, file)) as f:
        bboxes = json.load(f)

    new_tracks = []
    current_centroids = []

    
    for bbox in bboxes:
        min_bound = np.array(bbox["min_bound"])
        max_bound = np.array(bbox["max_bound"])
        centroid = (min_bound + max_bound) / 2.0
        current_centroids.append(centroid)

    current_centroids = np.array(current_centroids)

    assigned_ids = [-1] * len(current_centroids)
    if frame_num > 0 and len(current_centroids) > 0 and len(active_centroids) > 0:
        distances = cdist(current_centroids, active_centroids)
        for i, row in enumerate(distances):
            min_idx = np.argmin(row)
            if row[min_idx] < distance_threshold and min_idx not in assigned_ids:
                assigned_ids[i] = active_ids[min_idx]

 
    for i, aid in enumerate(assigned_ids):
        if aid == -1:
            aid = next_track_id
            next_track_id += 1
        bboxes[i]["track_id"] = aid
        new_tracks.append((aid, current_centroids[i]))


    with open(os.path.join(tracked_output_dir, file), "w") as f:
        json.dump(bboxes, f, indent=2)


    active_tracks = {tid: c for tid, c in new_tracks}
    active_ids = list(active_tracks.keys())
    active_centroids = np.array(list(active_tracks.values()))

    print(f"Frame {frame_num}: Tracked {len(bboxes)} objects.")
