
import cv2
import numpy as np
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_annotation.py <image_path> [output_svg_path]")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"Error: File not found {image_path}")
        sys.exit(1)

    if len(sys.argv) > 2:
        output_svg_path = sys.argv[2]
    else:
        output_svg_path = os.path.join(os.path.dirname(image_path), "raw_trace.svg")
    
    print(f"Processing {image_path}...")
    
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not read image")
        sys.exit(1)

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define colors (OpenCV HSV is H: 0-179, S: 0-255, V: 0-255)
    # Cyan: ~180 deg -> 90. Range 80-100 ?
    # Magenta: ~300 deg -> 150. Range 140-160 ?
    
    # Let's use fairly broad ranges but high saturation/value to pick up the digital colors
    
    # Cyan
    lower_cyan = np.array([80, 200, 200])
    upper_cyan = np.array([100, 255, 255])
    mask_cyan = cv2.inRange(hsv, lower_cyan, upper_cyan)

    # Magenta
    lower_magenta = np.array([140, 200, 200])
    upper_magenta = np.array([160, 255, 255])
    mask_magenta = cv2.inRange(hsv, lower_magenta, upper_magenta)

    # 1. Process Scale (Cyan)
    contours_cyan, _ = cv2.findContours(mask_cyan, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    pixels_per_mm = 0
    if not contours_cyan:
        print("Warning: No Cyan scale found!")
    else:
        # Assuming the largest cyan contour is the card
        c = max(contours_cyan, key=cv2.contourArea)
        rect = cv2.minAreaRect(c) # (center(x, y), (width, height), angle of rotation)
        width, height = rect[1]
        
        # ISO ID-1 size: 85.60 × 53.98 mm
        # We don't know which side is which in the rect, so match max to max
        max_px = max(width, height)
        min_px = min(width, height)
        
        # Calculate scale based on longer side (usually more reliable?)
        # Let's average both? Or just take the max.
        
        ppm_w = max_px / 85.60
        ppm_h = min_px / 53.98
        
        print(f"Cyan rect dimensions (px): {max_px:.2f} x {min_px:.2f}")
        print(f"Calculated PPM: Width-based={ppm_w:.2f}, Height-based={ppm_h:.2f}")
        
        # If they are very different, maybe it's not the card or perspective skew. 
        # For now, use max side as it likely corresponds to the 85.6mm if the card is mostly flat.
        pixels_per_mm = ppm_w
        print(f"Using Pixels per MM: {pixels_per_mm:.4f}")

    if pixels_per_mm == 0:
        print("Error: Could not determine scale. Aborting SVG generation with correct units.")
        # We could default to 1, but better to fail or warn?
        # Let's set 1 to produce pixel-based SVG
        pixels_per_mm = 1.0

    # 2. Process Trace (Magenta)
    contours_magenta, _ = cv2.findContours(mask_magenta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours_magenta:
        print("Error: No Magenta trace found!")
        sys.exit(1)
        
    # Combine all magenta contours or take largest?
    # Prompt implies "Draw a ... outline around the black plastic cover"
    # It might be one loop.
    c_magenta = max(contours_magenta, key=cv2.contourArea)
    
    # Simplify contour
    epsilon = 0.001 * cv2.arcLength(c_magenta, True)
    approx_curve = cv2.approxPolyDP(c_magenta, epsilon, True)
    
    # Convert pixels to mm
    points_mm = []
    
    # Image height for coordinate flip if needed (SVG usually top-left origin, same as image)
    # So (x, y) / ppm
    
    for point in approx_curve:
        x, y = point[0]
        points_mm.append((x / pixels_per_mm, y / pixels_per_mm))
        
    # Generate SVG content
    # ViewBox should cover the range. 
    # Let's offset so the top-left of the shape is near (0,0) or keep absolute?
    # Keeping absolute is safer for verifying against the image.
    
    # SVG size in mm
    h, w, _ = img.shape
    width_mm = w / pixels_per_mm
    height_mm = h / pixels_per_mm
    
    svg_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="{width_mm}mm"
   height="{height_mm}mm"
   viewBox="0 0 {width_mm} {height_mm}"
   xmlns="http://www.w3.org/2000/svg">
  <path
     d="M {points_mm[0][0]:.4f},{points_mm[0][1]:.4f} """
    
    for x, y in points_mm[1:]:
        svg_content += f"L {x:.4f},{y:.4f} "
        
    svg_content += """Z"
     style="fill:none;stroke:black;stroke-width:1" />
</svg>
"""

    with open(output_svg_path, 'w') as f:
        f.write(svg_content)
        
    print(f"Saved trace to {output_svg_path}")

if __name__ == "__main__":
    main()
