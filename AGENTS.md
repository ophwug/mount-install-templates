* Please keep the `.gitignore` file up to date. Do not leave cruft in the repository that `git status` will show.
* **NEVER** use deprecated models (e.g., `gemini-1.5-pro` or similar). Always use the latest available models as specified below.
* If Python is to be used, please use `uv` to manage dependencies.
* Use `uvx ruff check . --select F841,F401 --fix` to clean up unused variables and imports.
* Read the images of the PDFs generated afterwards to determine if they are sensible.
* Use `uv run tools/verify_build.py <image_path>` to verify the existence of arc lines using Gemini (requires Vertex AI environment).
* It should be possible to use `make -j 16` to build the PDFs in parallel quickly.
* Refer to https://docs.cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview
* Use `google-genai` for the Vertex AI SDK
* Maybe use `.env` or anything but make sure `GOOGLE_GENAI_USE_VERTEXAI=True` (This uses Vertex AI/GCP auth, NOT AI Studio/API Keys) . We are not using keys.
* Use `load_dotenv(override=True)` to ensure `.env` overrides system vars (critical for project/region switching)
* Use `gemini-3-flash-preview` for the chat/text/code model (only `global` location works here)
* For image manipulation, use `gemini-3-pro-image-preview` (only `global` location works here)
