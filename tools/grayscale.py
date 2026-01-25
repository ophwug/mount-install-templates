
import sys
from PIL import Image

def to_grayscale(input_path, output_path):
    try:
        img = Image.open(input_path).convert('L')
        img.save(output_path)
        print(f"Converted {input_path} to greyscale at {output_path}")
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python grayscale.py <input_image> <output_image>")
        sys.exit(1)
    
    to_grayscale(sys.argv[1], sys.argv[2])
