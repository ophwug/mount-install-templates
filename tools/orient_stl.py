#!/usr/bin/env -S uv run

import sys
import trimesh
import numpy as np

def orient_largest_face_down(input_file, output_file, flip=False):
    print(f"Loading {input_file}...")
    mesh = trimesh.load(input_file)
    
    # Compute stable poses
    transforms, probs = trimesh.poses.compute_stable_poses(mesh)
    
    if len(transforms) == 0:
        print("No stable poses found. Using original orientation.")
        mesh.export(output_file)
        return

    best_transform = transforms[np.argmax(probs)]
    
    print(f"Applying transformation for most stable pose (prob={np.max(probs):.2f})...")
    mesh.apply_transform(best_transform)

    if flip:
        print("Flipping 180 degrees (user override)...")
        # Rotate 180 around X axis
        flip_matrix = trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0])
        mesh.apply_transform(flip_matrix)

    # ---------------------------------------------------------
    # Refine Orientation: Landscape (Width > Height)
    # ---------------------------------------------------------
    # Get XY coordinates of all vertices
    xy_points = mesh.vertices[:, :2]
    
    # PCA is sensitive to vertex density and can result in slight rotation for asymmetric meshes.
    # Instead, we use the Minimum Area Rectangle of the 2D Convex Hull.
    from scipy.spatial import ConvexHull
    
    # 2D Convex Hull
    hull = ConvexHull(xy_points)
    hull_points = xy_points[hull.vertices]
    
    # Find geometric minimum area rectangle orientation
    min_area = float('inf')
    best_angle = 0.0
    
    # Iterate over all edges of the hull
    num_hull_points = len(hull_points)
    for i in range(num_hull_points):
        p1 = hull_points[i]
        p2 = hull_points[(i + 1) % num_hull_points]
        
        edge = p2 - p1
        # Angle of this edge relative to X-axis
        angle = np.arctan2(edge[1], edge[0])
        
        # Rotate hull points to alignment with X-axis to test AABB area
        c, s = np.cos(-angle), np.sin(-angle)
        # 2D Rotation matrix
        R = np.array([[c, -s], [s, c]])
        
        rotated_hull = hull_points @ R.T
        
        min_x = np.min(rotated_hull[:, 0])
        max_x = np.max(rotated_hull[:, 0])
        min_y = np.min(rotated_hull[:, 1])
        max_y = np.max(rotated_hull[:, 1])
        
        area = (max_x - min_x) * (max_y - min_y)
        
        if area < min_area:
            min_area = area
            best_angle = angle

    print(f"Aligning to Minimum Area Rectangle (Angle: {np.degrees(best_angle):.2f})...")
    # Rotate the actual mesh
    rotation_matrix = trimesh.transformations.rotation_matrix(-best_angle, [0, 0, 1])
    mesh.apply_transform(rotation_matrix)
    
    # Ensure Landscape (Width > Height)
    extents = mesh.extents
    if extents[1] > extents[0]: # Y > X
        print("Y extent > X extent. Rotating 90 degrees to enforce Landscape...")
        rot_90 = trimesh.transformations.rotation_matrix(np.pi/2, [0, 0, 1])
        mesh.apply_transform(rot_90)
    
    # ---------------------------------------------------------
    # Refine Orientation: "Widest Side At Top"
    # ---------------------------------------------------------
    # Heuristic: Check width at Y_max vs Y_min.
    # We want Width(Y_max) > Width(Y_min).
    
    # Re-fetch vertices after rotation
    xy_points = mesh.vertices[:, :2]
    y_vals = xy_points[:, 1]
    x_vals = xy_points[:, 0]
    
    min_y, max_y = np.min(y_vals), np.max(y_vals)
    tolerance = (max_y - min_y) * 0.1 # Look at top/bottom 10% slices
    
    # Get points in top slice
    top_mask = y_vals > (max_y - tolerance)
    if np.any(top_mask):
        top_width = np.max(x_vals[top_mask]) - np.min(x_vals[top_mask])
    else:
        top_width = 0
        
    # Get points in bottom slice
    bottom_mask = y_vals < (min_y + tolerance)
    if np.any(bottom_mask):
        bottom_width = np.max(x_vals[bottom_mask]) - np.min(x_vals[bottom_mask])
    else:
        bottom_width = 0
        
    print(f"Top Width: {top_width:.2f}, Bottom Width: {bottom_width:.2f}")
    
    if bottom_width > top_width:
        print("Bottom is wider than top. Rotating 180 degrees to put widest side at top...")
        rot_180 = trimesh.transformations.rotation_matrix(np.pi, [0, 0, 1])
        mesh.apply_transform(rot_180)
    
    # ---------------------------------------------------------
    # Z-Level Adjustment
    # ---------------------------------------------------------
    bounds = mesh.bounds
    min_z = bounds[0][2]
    
    print(f"Min Z after transform: {min_z}")
    
    if not np.isclose(min_z, 0):
        mesh.apply_translation([0, 0, -min_z])
    
    print(f"Saving to {output_file}...")
    mesh.export(output_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("--flip", action="store_true", help="Flip 180 degrees (upside down) before processing")
    args = parser.parse_args()
        
    orient_largest_face_down(args.input_file, args.output_file, flip=args.flip)
