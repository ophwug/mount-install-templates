> [!WARNING]
> **RFC / WORK IN PROGRESS**
> This project is currently a Request For Comments (RFC). The dimensions and clearance zones are **guesswork** and have not been validated with final hardware. **Do not rely on these templates for critical cutting/installation without verifying measurements yourself.**

# Install Templates for comma.ai hardware

Inspired by [Apple's Apple Watch band size](https://www.apple.com/shop/Catalog/US/Images/bxxd/size-guide_CA.pdf). 

* Users can check for correct sizing of generated PDFs with an outline of a credit or ID card.
* Users can visit a HTML page hosted on GitHub Pages to see the list of PDFs.
* Page generates a PDF for each mount in [commaai/hardware](https://github.com/commaai/hardware) for comma three, comma 3x, and comma four.

## Download Templates
| Mount | Orientation | US Letter (PDF) | A4 (PDF) |
| :--- | :--- | :--- | :--- |
| **comma three** | Portrait | [Download](https://ophwug.github.io/install-templates/c3_mount.pdf) | [Download](https://ophwug.github.io/install-templates/c3_mount_a4.pdf) |
| | Landscape | [Download](https://ophwug.github.io/install-templates/c3_mount_landscape.pdf) | [Download](https://ophwug.github.io/install-templates/c3_mount_a4_landscape.pdf) |
| **comma 3x** | Portrait | [Download](https://ophwug.github.io/install-templates/c3x_mount.pdf) | [Download](https://ophwug.github.io/install-templates/c3x_mount_a4.pdf) |
| | Landscape | [Download](https://ophwug.github.io/install-templates/c3x_mount_landscape.pdf) | [Download](https://ophwug.github.io/install-templates/c3x_mount_a4_landscape.pdf) |
| **comma four** | Portrait | [Download](https://ophwug.github.io/install-templates/four_mount.pdf) | [Download](https://ophwug.github.io/install-templates/four_mount_a4.pdf) |
| | Landscape | [Download](https://ophwug.github.io/install-templates/four_mount_landscape.pdf) | [Download](https://ophwug.github.io/install-templates/four_mount_a4_landscape.pdf) |

## How to Use
This project generates PDF templates to help mount comma hardware correctly.

### 1. Printing
*   **Print at 100% Scale**: Ensure that "Scale to Fit" or "Shrink to Fit" is **disabled** in your printer settings.
*   **Paper Size**: Templates are designed for **US Letter**.

### 2. Verify Scale
*   Place a standard **credit card or ID card** in the marked box at the bottom of the page.
*   If the card fits exactly within the box, the scale is correct. **If it doesn't fit, do not use the template.**

### 3. Preparation & Positioning
*   **Cutting**: You can cut the template however you see fit. Usually, cutting around the mount footprint and leaving the clearance arcs intact is best.
*   **Clearance Zone**: The red dashed arcs indicate the required clearance from the **top of the mount** to the **vehicle's original camera housing**.
*   The camera housing should be **outside** (above) the curved arcs for an unobstructed view. Arcs range from **300mm** to **1000mm**.

### 4. Installation
*   Align the mount footprint on your windshield.
*   Mark the corners on the glass (e.g., with a dry-erase marker) or use painters tape to temporarily hold the template in place.
*   Follow standard comma.ai instructions to attach the mount using the provided adhesive.

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
    *   **comma three / 3x**: **35mm** from top of mount to start of clearance zone.
    *   **comma four**: **44mm** from top of mount to start of clearance zone.

### Tools Required

To build the templates locally, you will need:

*   [OpenSCAD](https://openscad.org/) (headless support required)
*   [Typst](https://typst.app/)
*   Python 3 with `numpy-stl`
*   Make
