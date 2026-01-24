#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "google-cloud-aiplatform",
#   "pillow",
# ]
# ///

import os
import sys
import vertexai
from vertexai.generative_models import GenerativeModel, Image as VertexImage
from PIL import Image
import io

def verify_image(image_path):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION") or os.environ.get("LOCATION") or "us-central1"

    if not project_id:
        print("Error: GOOGLE_CLOUD_PROJECT environment variable not set.")
        sys.exit(1)

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-2.0-flash-exp")

    print(f"Analyzing {image_path} using Gemini 2.0 Flash on Vertex AI (Project: {project_id}, Location: {location})...")
    
    # Load image for Vertex AI
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    
    img = VertexImage.from_bytes(img_bytes)
    
    prompt = """
    Look at this image of a mounting template. 
    1. Above the central oval shape, there is a "Vehicle's Original Camera Housing" marked by a horizontal red line. 
       Are there dashed red arc lines visible ABOVE this line?
    2. At the bottom, there is a "Credit Card Scale" box. 
       Is the main mounting template (oval, line, or arcs) colliding with or overlapping this credit card box?
    
    Please answer with "Yes/No" for both points, followed by a brief reason.
    """

    response = model.generate_content([prompt, img])
    print(f"Gemini Report: {response.text.strip()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./verify_build.py <image_path>")
        sys.exit(1)
    
    verify_image(sys.argv[1])
