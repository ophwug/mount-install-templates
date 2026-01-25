* Please kept the `.gitignore` file up to date. Do not leave cruft in the repository that `git status` will show.
* If Python is to be used, please use `uv` to manage dependencies.
* Read the images of the PDFs generated afterwards to determine if they are sensible.
* Use `uv run tools/verify_build.py <image_path>` to verify the existence of arc lines using Gemini (requires Vertex AI environment).
* It should be possible to use `make -j` to build the PDFs in parallel.