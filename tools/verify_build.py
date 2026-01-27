#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "google-genai",
#   "python-dotenv",
#   "pillow",
# ]
# ///

import os
import sys
import glob
from google import genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv(override=True)

def verify_image(client, image_path):
    model_id = "gemini-3-flash-preview" 

    print(f"Analyzing {image_path} using {model_id}...")
    
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return False

    prompt = """
    Analyze this mounting template image.
    1. Are there RED DASHED LINES indicating a clearance zone? (They should be shaped like a camera cover trace).
    2. Is there a "Vehicle's Original Camera Housing" label?
    3. Is there a credit card scale box?
    4. Is the text legible?
    
    Answer YES or NO for each, and provide a short summary.
    If any of these are NO, say "FAIL". Otherwise "PASS".
    """

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=[image, prompt]
        )
        report = response.text.strip()
        print(f"Gemini Report:\n{report}")
        return "PASS" in report
    except Exception as e:
        print(f"Error during generation: {e}")
        return False

def main():
    # Standard setup from AGENTS.md
    if os.environ.get("GOOGLE_GENAI_USE_VERTEXAI") == "True":
        print("Using Vertex AI...")
        client = genai.Client(
            vertexai=True,
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location="global"
        )
    else:
        print("Using AI Studio...")
        client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    files_to_check = []
    if len(sys.argv) > 1:
        files_to_check = sys.argv[1:]
    else:
        # Check all build PNGs if no args
        base_dir = "build"
        if os.path.exists(base_dir):
            files_to_check.extend(glob.glob(os.path.join(base_dir, "*.png")))
            files_to_check.extend(glob.glob(os.path.join(base_dir, "vehicles", "*", "*.png")))
            # Filter out bw images if desired? User said "spot check all". 
            # Usually we check the main ones. Let's exclude _bw.png to save time/cost unless requested?
            # User said "spot check all the vehicle ones too".
            # Checking color ones is probably best for red lines check.
            files_to_check = [f for f in files_to_check if "_bw.png" not in f]

    if not files_to_check:
        print("No files found to verify.")
        sys.exit(0)

    print(f"Verifying {len(files_to_check)} files in parallel...")
    
    import concurrent.futures

    failed = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {executor.submit(verify_image, client, f): f for f in files_to_check}
        for future in concurrent.futures.as_completed(future_to_file):
            f = future_to_file[future]
            try:
                if not future.result():
                    failed.append(f)
            except Exception as exc:
                print(f"{f} generated an exception: {exc}")
                failed.append(f)
    
    if failed:
        print(f"\nVerification FAILED for: {failed}")
        sys.exit(1)
    else:
        print("\nAll checks PASSED.")

if __name__ == "__main__":
    main()
