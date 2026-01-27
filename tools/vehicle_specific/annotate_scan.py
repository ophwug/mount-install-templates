
import os
import sys
from dotenv import load_dotenv
from google import genai
from PIL import Image

def main():
    # Load environment variables
    load_dotenv(override=True)

    # Check/Set environment variables for Vertex AI
    if not os.environ.get("GOOGLE_GENAI_USE_VERTEXAI"):
        print("Warning: GOOGLE_GENAI_USE_VERTEXAI not set. Defaulting to True as per AGENTS.md", file=sys.stderr)
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print("Warning: GOOGLE_CLOUD_PROJECT not set. Please set it in .env", file=sys.stderr)
    
    if not os.environ.get("GOOGLE_CLOUD_LOCATION"):
        print("Warning: GOOGLE_CLOUD_LOCATION not set. Defaulting to 'global'", file=sys.stderr)
        os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

    # Get image path from args or default
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("Usage: annotate_scan.py <image_path> [output_path]")
        sys.exit(1)
    
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        output_path = None

    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Processing image: {image_path}")

    # Read image
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}", file=sys.stderr)
        sys.exit(1)

    # Initialize client
    client = genai.Client(
        vertexai=True,
        location="global"
    )

    prompt = "Draw a bold, 5px wide solid Magenta outline around the black plastic cover, and a bold, 5px wide solid Cyan outline around the ISO standard-sized card (such as a credit card)."

    print("Sending request to Gemini...")
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[prompt, image],
        )
        
        if response.text:
             print(f"Model returned text instead of image: {response.text}")

        # specific handling for image response might be needed depending on SDK version, 
        # but typically binary content is in parts or directly accessible if configured.
        # However, for 'image-preview' models and image generation, the response handling might differ.
        # Let's try to save the raw bytes if present.
        
        # Based on SDK common patterns for image generation/editing:
        # The response should contain the image data.
        
        # Let's inspect the response structure if we were debugging, but here we write likely code.
        # Assuming the standard response object has `bytes` or we iterate parts.
        
        # For now, let's look for inline data.
        
        base_dir = os.path.dirname(image_path)
        base_name = os.path.basename(image_path)
        
        if output_path:
            output_file = output_path
        else:
            output_filename = f"annotated_{base_name}"
            # Attempt to put in 'ai' folder if input is in 'raw'
            if base_dir.endswith("raw"):
                ai_dir = base_dir.replace("raw", "ai")
                if not os.path.exists(ai_dir):
                    os.makedirs(ai_dir)
                output_file = os.path.join(ai_dir, output_filename)
            else:
                output_file = os.path.join(base_dir, output_filename)
        
        # Check if we got a valid response with bytes
        # Note: The SDK shape might verify, but let's assume standard `response.bytes` or similar for generated media won't work 
        # directly for image-to-image without looking at the parts.
        
        # Actually, for image editing/generation, usually we look at candidates[0].content.parts[0].inline_data
        
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                img_data = part.inline_data.data
                with open(output_file, "wb") as f:
                    f.write(img_data)
                print(f"Saved annotated image to {output_file}")
                return

        print("No image data found in response.")


    except Exception as e:
        print(f"Error calling Gemini: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
