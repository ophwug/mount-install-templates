#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "trimesh",
#   "numpy",
#   "scipy",
#   "networkx",
# ]
# ///

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
    
    # PCA for primary axis alignment
    centered_points = xy_points - np.mean(xy_points, axis=0)
    cov_matrix = np.cov(centered_points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    primary_axis = eigenvectors[:, -1]
    
    # Align to X
    angle_to_x = np.arctan2(primary_axis[1], primary_axis[0])
    print(f"Rotating by {-np.degrees(angle_to_x):.2f} degrees to align primary axis with X...")
    rotation_matrix = trimesh.transformations.rotation_matrix(-angle_to_x, [0, 0, 1])
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
