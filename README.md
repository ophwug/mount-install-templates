# Install Templates for comma.ai hardware

Inspired by [Apple's Apple Watch band size](https://www.apple.com/shop/Catalog/US/Images/bxxd/size-guide_CA.pdf). 

* Users can check for correct sizing of generated PDFs with an outline of a credit or ID card.
* Users can visit a HTML page hosted on GitHub Pages to see the list of PDFs.
* Page generates a PDF for each mount in [comma.ai's hardware repository](https://github.com/commaai/hardware) for comma three, comma 3x, and comma four.

## Download Templates
| Mount | PDF Template | Preview |
| :--- | :--- | :--- |
| **Comma Three (Standard)** | [Download PDF](https://ophwug.github.io/install-templates/c3_mount.pdf) | ![Preview](https://ophwug.github.io/install-templates/c3_mount.png) |
| **Comma 3X (Standard)** | [Download PDF](https://ophwug.github.io/install-templates/c3x_mount.pdf) | ![Preview](https://ophwug.github.io/install-templates/c3x_mount.png) |
| **Comma Four** | [Download PDF](https://ophwug.github.io/install-templates/four_mount.pdf) | ![Preview](https://ophwug.github.io/install-templates/four_mount.png) |

## Technical

* Has a submodule for the hardware repo.
* Has a makefile to generate the PDFs and HTML page.
* Uses openscad to project a 3D model of the mount's bottom layer to a 2D plane to produce a SVG.
* Uses Typst to create a PDF with the SVG and a outline of a credit card for scale.
* Puts multiple 300-600mm radius lines above the mount to ensure the user can still slide out their device after mounting.
* Distance for comma three and comma 3x is 60mm to the lines above.
* Distance for comma four is 80mm to the lines above.
