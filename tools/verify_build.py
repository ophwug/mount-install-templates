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
    Look at this image of a mounting template and verify the following:
    1. At the top, is there a label reading "Vehicle's Original Camera Housing" 20mm above a horizontal red line? 
       Are there dashed red arc lines visible ABOVE this label?
    2. In the center of the main mounting template (the oval/irregular shape), is there a bold label reading "comma mount" split over two lines?
    3. In the footer area, is there a descriptive text that starts with "This is a template to help people mount comma devices..."?
    4. At the bottom, is there a "Credit Card Scale" box? 
    5. Overall Layout: Are any text elements, lines, or the mounting template shape colliding with each other or the credit card box? 
       Is there a clear margin (approx 1cm) around the edges of the page?
    
    Please answer with "Yes/No" for each point, followed by a brief reason for any "No" answers.
    """

    response = model.generate_content([prompt, img])
    print(f"Gemini Report: {response.text.strip()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./verify_build.py <image_path>")
        sys.exit(1)
    
    verify_image(sys.argv[1])
