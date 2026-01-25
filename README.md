# Mount Installation Templates for comma.ai devices

*Mounting your comma device correctly the first time for best results.*

This tool is inspired by [Apple's Apple Watch band size tool for people who are too cool for straps with holes](https://www.apple.com/shop/Catalog/US/Images/bxxd/size-guide_CA.pdf). 

* Users can check for correct sizing of generated PDFs with an outline of a credit or ID card.
* Users can see the list of PDFs in the [Download Templates](#download-templates) section below.
* Page generates a PDF for each mount's footprint in [commaai/hardware](https://github.com/commaai/hardware) for comma three, comma 3x, and comma four.

## Download Templates

All templates are standardized in **Landscape** orientation for maximum clarity and compatibility.

### comma three
*   [US Letter Landscape](https://ophwug.github.io/install-templates/c3_mount.pdf)
*   [A4 Landscape](https://ophwug.github.io/install-templates/c3_mount_a4.pdf)

### comma 3x
*   [US Letter Landscape](https://ophwug.github.io/install-templates/c3x_mount.pdf)
*   [A4 Landscape](https://ophwug.github.io/install-templates/c3x_mount_a4.pdf)

### comma four
*   [US Letter Landscape](https://ophwug.github.io/install-templates/four_mount.pdf)
*   [A4 Landscape](https://ophwug.github.io/install-templates/four_mount_a4.pdf)

## How to Use
This project generates PDF mount installation templates to help mount comma hardware correctly.

### 1. Printing
*   **Print at 100% Scale**: Ensure that "Scale to Fit" or "Shrink to Fit" is **disabled** in your printer settings.
*   **Paper Size**: Templates are available for both **US Letter** and **A4** paper sizes. Choose the appropriate version for your region from the [Download Templates](#download-templates) list above.

### 2. Verify Scale
*   Place a standard **credit card or ID card** in the marked box at the bottom of the page.
*   If the card fits exactly within the box, the scale is correct. **If it doesn't fit, do not use the template.**

### 3. Installation & Positioning
*   **Recommended Method (Outside Taping)**: Tape the template to the **outside** of the windshield! This makes it much easier to align with the camera/mirror from the inside without the paper getting in the way of your level or tape measure. Since you can't see the other side, you may want to have a very bright light source inside the car to see the template or a helper.
*   **Alternative Method (Cutting)**: If taping to the outside doesn't work for you, you can cut the template however you see fit. Usually, cutting around the mount footprint and leaving the clearance arcs intact is best.
*   **Clearance Zone**: The red dashed arcs indicate the required clearance from the **top of the mount** to the **vehicle's original camera housing**.
*   The camera housing should be **outside** (above) the curved arcs for an unobstructed view. Arcs range from **300mm** to **1000mm**.
*   Mark the corners on the glass (e.g., with a dry-erase marker) or use painters tape to temporarily hold the template in place.
*   Follow standard comma.ai instructions to attach the mount using the provided adhesive.

## Technical Details

### Build Pipeline

The PDF generation process is automated using `make`.

1.  **Source**: Mount models (`.stl`) are sourced from the [commaai/hardware](https://github.com/commaai/hardware) submodule.
2.  **Orientation**: The `tools/orient_stl.py` Python script loads each STL and rotates it to align the mounting surface with the XY plane (flat).
3.  **Projection**: `openscad` is invoked with `tools/project_mount.scad` to project the very bottom of the 3D geometry onto a 2D plane, exporting the footprint as an SVG.
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
*   Python 3 with `numpy-stl`, though `uv` is used to manage dependencies.
*   Make

Those tools can be found in package managers such as `brew` on macOS, `apt` on Debian/Ubuntu, `dnf` on Fedora, etc.
