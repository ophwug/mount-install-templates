> [!WARNING]
> **RFC / WORK IN PROGRESS**
> This project is currently a Request For Comments (RFC). The dimensions and clearance zones are **guesswork** and have not been validated with final hardware. **Do not rely on these templates for critical cutting/installation without verifying measurements yourself.**

# Install Templates for comma.ai hardware

Inspired by [Apple's Apple Watch band size](https://www.apple.com/shop/Catalog/US/Images/bxxd/size-guide_CA.pdf). 

* Users can check for correct sizing of generated PDFs with an outline of a credit or ID card.
* Users can visit a HTML page hosted on GitHub Pages to see the list of PDFs.
* Page generates a PDF for each mount in [comma.ai's hardware repository](https://github.com/commaai/hardware) for comma three, comma 3x, and comma four.

## Download Templates
| Mount | PDF Template |
| :--- | :--- |
| **Comma Three (Standard)** | [Download PDF](https://ophwug.github.io/install-templates/c3_mount.pdf) |
| **Comma 3X (Standard)** | [Download PDF](https://ophwug.github.io/install-templates/c3x_mount.pdf) |
| **Comma Four** | [Download PDF](https://ophwug.github.io/install-templates/four_mount.pdf) |

## Technical Details

### Build Pipeline

The PDF generation process is automated using `make`.

1.  **Source**: Mount models (`.stl`) are sourced from the [commaai/hardware](https://github.com/commaai/hardware) submodule.
2.  **Orientation**: The `tools/orient_stl.py` Python script loads each STL and rotates it to align the mounting surface with the XY plane (flat).
3.  **Projection**: `openscad` is invoked with `tools/project_mount.scad` to project the 3D geometry onto a 2D plane, exporting the footprint as an SVG.
4.  **Composition**: `typst` compiles `template.typ`, which combines the generated SVG footprint with:
    -   A credit card outline for scale validation.
    -   Clearance zone markings.
    -   Title and instructional text.

### Specifications

*   **Fonts**: Uses `DejaVu Sans Mono`.
*   **Clearance Zones**: Dashed red arcs indicate required clearance radii at **300mm**, **400mm**, **500mm**, and **600mm**.
*   **Clearance Offsets**:
    *   **Comma Three / 3X**: **60mm** from top of mount to start of clearance zone.
    *   **Comma Four**: **80mm** from top of mount to start of clearance zone.

### Tools Required

To build the templates locally, you will need:

*   [OpenSCAD](https://openscad.org/) (headless support required)
*   [Typst](https://typst.app/)
*   Python 3 with `numpy-stl`
*   Make
