#!/bin/bash
# Visualize PDFs as PNGs

BUILD_DIR="build"

echo "Converting PDFs to PNGs..."

for pdf in "$BUILD_DIR"/*.pdf; do
    [ -e "$pdf" ] || continue
    filename=$(basename "$pdf" .pdf)
    echo "  $filename.pdf -> $filename.png"
    pdftoppm -png -singlefile "$pdf" "$BUILD_DIR/$filename"
done

echo "Done."
