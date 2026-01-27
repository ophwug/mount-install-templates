
import sys
import os
import re
import numpy as np

def parse_svg_path_points(svg_path):
    with open(svg_path, 'r') as f:
        content = f.read()
    
    match = re.search(r'd="([^"]+)"', content)
    if not match:
        raise ValueError("Could not find path data in SVG")
    
    d_str = match.group(1)
    parts = re.split(r'[ ,a-zA-Z]+', d_str)
    numbers = [float(p) for p in parts if p.strip()]
    
    points = []
    for i in range(0, len(numbers), 2):
        if i+1 < len(numbers):
            points.append([numbers[i], numbers[i+1]])
            
    return np.array(points)

def write_svg(points, output_path):
    min_x = np.min(points[:, 0])
    max_x = np.max(points[:, 0])
    min_y = np.min(points[:, 1])
    max_y = np.max(points[:, 1])
    
    width = max_x - min_x
    height = max_y - min_y
    
    margin = 5
    min_x -= margin
    min_y -= margin
    width += 2*margin
    height += 2*margin
    
    svg_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="{width}mm"
   height="{height}mm"
   viewBox="{min_x} {min_y} {width} {height}"
   xmlns="http://www.w3.org/2000/svg">
  <path
     d="M {points[0][0]:.4f},{points[0][1]:.4f} """
    
    for p in points[1:]:
        svg_content += f"L {p[0]:.4f},{p[1]:.4f} "
        
    svg_content += """Z"
     style="fill:none;stroke:black;stroke-width:1" />
</svg>
"""
    with open(output_path, 'w') as f:
        f.write(svg_content)

def get_intersections(y, points):
    intersections = []
    num_points = len(points)
    for i in range(num_points):
        p1 = points[i]
        p2 = points[(i + 1) % num_points]
        
        y_min = min(p1[1], p2[1])
        y_max = max(p1[1], p2[1])
        
        # Check if segments cross Y
        # Use slightly tolerant bounds to avoid missing exact vertex hits or use half-open intervals
        if y_min <= y and y <= y_max and (y_max - y_min) > 1e-9:
            # Linear interpolation
            # x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
            intersections.append(x)
            
    return sorted(intersections)

def main():
    if len(sys.argv) < 2:
        print("Usage: python refine_trace.py <input_svg_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"Error: File not found {input_path}")
        sys.exit(1)

    output_path = os.path.join(os.path.dirname(input_path), "trace.svg")
    
    print(f"Reading {input_path}...")
    points = parse_svg_path_points(input_path)
    
    # 1. Rotate 180 degrees and Center
    centroid = np.mean(points, axis=0)
    centered_points = points - centroid
    rotated_points = -centered_points
    
    # Re-center Y range to start near 0 for debugging clarity logic
    # Find min Y
    min_y = np.min(rotated_points[:, 1])
    max_y = np.max(rotated_points[:, 1])
    
    # 2. Geometric Slicing
    # Step through Y indices
    # We want a smooth curve, so high resolution
    num_slices = 200
    y_levels = np.linspace(min_y, max_y, num_slices)
    
    left_profile = []
    right_profile = []
    
    # Ensure points are processed as a closed loop
    
    for y in y_levels:
        xs = get_intersections(y, rotated_points)
        
        # We expect even number of intersections, usually 2 for a convex-ish shape
        if len(xs) >= 2:
            # Take min and max as the outer bounds
            min_x = xs[0]
            max_x = xs[-1]
            width = max_x - min_x
            
            # Symmetrize width
            half_width = width / 2
            
            left_profile.append([-half_width, y])
            right_profile.append([half_width, y])
            
    # Combine
    # Left profile goes top to bottom (y increasing)
    # Right profile goes top to bottom (y increasing)
    # To form a loop:
    # Top -> Left (down) -> Bottom -> Right (up) -> Top
    
    # left_profile has Y increasing.
    # right_profile has Y increasing.
    
    # Loop order:
    # 1. Left profile (reversed? No, standard polygon order often checks winding)
    # Let's start from Top.
    # Top-most point is first in list.
    
    # Left side: Traverse from top (index 0) to bottom (index -1)
    # Right side: Traverse from bottom (index -1) to top (index 0)
    
    final_points_left = np.array(left_profile)
    final_points_right = np.array(right_profile)[::-1] # Reverse right side
    
    if len(final_points_left) == 0:
         print("Error: No valid intersections found.")
         sys.exit(1)

    final_points = np.concatenate([final_points_left, final_points_right])

    # 3. Save
    write_svg(final_points, output_path)
    print(f"Saved refined trace to {output_path}")

if __name__ == "__main__":
    main()
