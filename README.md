# Mount Installation Templates for comma.ai devices

![Comma Four Template Preview](https://ophwug.github.io/mount-install-templates/c4_mount_letter.png)

*Mounting your comma device correctly the first time for best results.*

> [!IMPORTANT]
> **Disclaimer:** These are **NOT** official comma.ai templates. This is a community-made project.
> Please direct all issues, suggestions, and feedback to the Issues tab of this repository.


This tool is inspired by [Apple's Apple Watch band size tool for people who are too cool for straps with holes](https://www.apple.com/shop/Catalog/US/Images/bxxd/size-guide_CA.pdf) and [Toyota's OEM Dashcam installation instructions](https://www.4runner6g.com/forum/threads/oem-toyota-dashcam-diy-how-to-install-instructions-and-how-to-remove-map-dome-light-console.2603/).

* Users can check for correct sizing of generated PDFs with an outline of a credit or ID card.
* Users can see the list of PDFs in the [Download Templates](#download-templates) section below.
* We programmatically generate a PDF for each mount's footprint in [commaai/hardware](https://github.com/commaai/hardware) for comma three, comma 3x, and comma four.

## Download Templates

All templates are standardized in **Landscape** orientation for maximum clarity and compatibility.

### comma four
*   [US Letter Landscape](https://ophwug.github.io/mount-install-templates/c4_mount_letter.pdf)
*   [A4 Landscape](https://ophwug.github.io/mount-install-templates/c4_mount_a4.pdf)

### comma 3x
*   [US Letter Landscape](https://ophwug.github.io/mount-install-templates/c3x_mount_letter.pdf)
*   [A4 Landscape](https://ophwug.github.io/mount-install-templates/c3x_mount_a4.pdf)

### comma three
*   [US Letter Landscape](https://ophwug.github.io/mount-install-templates/c3_mount_letter.pdf)
*   [A4 Landscape](https://ophwug.github.io/mount-install-templates/c3_mount_a4.pdf)

## Vehicle Specific Templates

These templates feature custom clearance zones (red dashed lines) derived from actual vehicle scans, offering precise alignment guides for specific car models.

> [!WARNING]
> **Beta Feature:** These templates are experimental and derived from user scans. Always double-check measurements before permanent installation.

> [!NOTE]
> **Want to help?** We're looking for contributions to expand our vehicle-specific template library! Please submit a flatbed scanner scan of your car's ADAS camera cover (after removing it from the vehicle) along with a card-sized object for scale (e.g., gift card, library card, or any standard credit card-sized item). Share your scans or suggestions at [Issue #6](https://github.com/ophwug/mount-install-templates/issues/6).

### Toyota Corolla (2020)
#### comma four
*   [US Letter](https://ophwug.github.io/mount-install-templates/vehicles/2020_corolla/c4_mount_letter.pdf) | [A4](https://ophwug.github.io/mount-install-templates/vehicles/2020_corolla/c4_mount_a4.pdf)
#### comma 3x
*   [US Letter](https://ophwug.github.io/mount-install-templates/vehicles/2020_corolla/c3x_mount_letter.pdf) | [A4](https://ophwug.github.io/mount-install-templates/vehicles/2020_corolla/c3x_mount_a4.pdf)
#### comma three
*   [US Letter](https://ophwug.github.io/mount-install-templates/vehicles/2020_corolla/c3_mount_letter.pdf) | [A4](https://ophwug.github.io/mount-install-templates/vehicles/2020_corolla/c3_mount_a4.pdf)

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

### AI / Computer Vision Workflow

An experimental workflow exists to trace vehicle features (like camera covers) from scans using Gemini and OpenCV. The entire pipeline is automated via `make`.

1.  **Preparation**: Place a scan of the car's ADAS camera cover (after removing it from the vehicle) with a card-sized object for scale (e.g., gift card, library card, or any standard credit card-sized item) in `vehicles/<vehicle_name>/raw/scan.png`.
2.  **Annotate**: Run `make annotate-<vehicle_name>` (e.g. `make annotate-2020_corolla`) to trigger the AI annotation. `tools/vehicle_specific/annotate_scan.py` uses Gemini 3 Pro (image-preview) to highlight features (Magenta) and scale cards (Cyan), saving to `vehicles/<vehicle_name>/ai/annotated_scan.png`.
3.  **Process**: `tools/vehicle_specific/process_annotation.py` extracts the scale (pixels/mm) and the raw trace from the annotated image to `vehicles/<vehicle_name>/gen/raw_trace.svg`.
4.  **Refine**: `tools/vehicle_specific/refine_trace.py` rotates, centers, and symmetrizes the trace for engineering use, saving to `vehicles/<vehicle_name>/gen/trace.svg`.
5.  **Offsets**: `tools/vehicle_specific/generate_offsets.py` adds clearance lines and the centerline, creating the final `vehicles/<vehicle_name>/gen/offsets.svg` used in the template.
6.  **Verify**: `make verify` runs `tools/verify_build.py`, which uses **Gemini 3 Flash** to visually inspect all generated PDFs/PNGs. It checks for the presence of red clearance lines, correct labels, and legible text, failing the build if any template is suspect.

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
*   Python 3 with `numpy-stl`, though [`uv`](https://docs.astral.sh/uv/) is used to manage dependencies.
*   Make

Those tools can be found in package managers such as `brew` on macOS, `apt` on Debian/Ubuntu, `dnf` on Fedora, etc.

## Adhesive Cutting Templates

Here are 3D printable STL files that can serve as cutting guides for mount adhesives. These are particularly useful if you are replacing the 3M VHB adhesive and want a perfect fit for the mount's footprint.

![Adhesive Cutting Template Preview](https://github.com/ophwug/mount-install-templates/raw/main/build/c4_cutting_template_preview.png)

*   **comma four**: [Standard (with islands)](https://github.com/ophwug/mount-install-templates/raw/main/build/c4_cutting_template.stl) | [Solid (no islands)](https://github.com/ophwug/mount-install-templates/raw/main/build/c4_cutting_template_solid.stl)
*   **comma 3x**: [Standard (with islands)](https://github.com/ophwug/mount-install-templates/raw/main/build/c3x_cutting_template.stl) | [Solid (no islands)](https://github.com/ophwug/mount-install-templates/raw/main/build/c3x_cutting_template_solid.stl)
*   **comma three**: [Standard](https://github.com/ophwug/mount-install-templates/raw/main/build/c3_cutting_template.stl)

The standard templates for comma four and 3x include split horizontal bridges to support internal island guides (for the mount's own internal relief holes) while keeping the central area clear. The solid versions provide just the outer silhouette.

## Similar Tools

* [DML Tool](https://publish.obsidian.md/typedbyhumans/Folders/comma/DML+Tool) - A 3D printed tool with additional added components such as a mini-level bubble tool to help make sure the mount is leveled on the windshield.