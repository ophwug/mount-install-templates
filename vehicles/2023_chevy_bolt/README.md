# 2023 Chevy Bolt scan provenance

Source: [zikeji's contribution to issue #6](https://github.com/ophwug/mount-install-templates/issues/6#issuecomment-4283816153)
and [source commit 9e481ce](https://github.com/zikeji/mount-install-templates/tree/9e481cede1872b4de8dedfb96c7f349ea29c89c9/vehicles/2023_chevy_bolt).
The original scan, AI annotation, vehicle name, and starter template are preserved from that branch.

The contributor described a “'23 Chevy Bolt Premier.” Exact EV/EUV identification
and trim applicability have not been verified; these templates use the submitted
2023 Chevy Bolt name and are experimental. No physical fit validation has been
reported for this version.

## Geometry

`tools/vehicle_specific/trace_bolt_scan.py` reads the original 5100 x 6600 scan.
It fits the two short edges of the reference card and uses their perpendicular
separation as 85.60mm, assuming a standard ID-1 card. The PNG has no DPI metadata.
The card's actual physical dimensions must be checked by the contributor; the
PDF's printed credit-card check only verifies printer scaling.

The script extracts the dark housing's lower rounded edge from an explicit pixel
region, corrects the small scan rotation using its broad lower section, and
simplifies the open polyline with a 0.15mm tolerance. It does not infer the blurred
interior, mirror opening, or hidden geometry. The SVG displays the bottom 15mm
of that edge with the same 5mm bottom padding expected by the shared template.
The traced edge's horizontal midpoint is centered on the page. It is not a
measurement of the vehicle centerline or camera position. Confirm the cover's
orientation and position in the vehicle before using the guide.

The supplied AI annotation is kept for provenance but is not used for scale or
geometry. Its magenta stroke is open: the generic contour extractor follows both
sides of the stroke, and the generic refiner then rotates 180 degrees and forces
symmetry. That is unsuitable for this scan and can introduce spurious geometry.

Regenerate with `uv run tools/vehicle_specific/trace_bolt_scan.py`, or let `make`
rebuild `gen/offsets.svg` from its scan/script prerequisites. Do not run the generic
annotation/refinement pipeline over the Bolt output.

## Build

From the repository root:

```sh
make update-hardware
make -j 16 INDIVIDUAL=1 build/vehicles/2023_chevy_bolt/c4_mount_55mm_letter.pdf build/vehicles/2023_chevy_bolt/c4_mount_55mm_letter.png
```

`make -j 16 vehicles` includes all three comma mounts, both paper sizes, the
legacy default offsets, and the 45/50/55/60/65mm variants. Fitment and removal
clearance still need confirmation on the vehicle; these offsets are choices,
not a vehicle-specific recommendation.

`make` generates the mount SVG prerequisites; Bolt tracing does not require
Vertex AI. Local validation used OpenSCAD 2026.03.01 (CI uses nightly); older
CGAL builds have a reported C3X projection failure in issue #6.

Regression checks: `uv run -m unittest tools.vehicle_specific.test_trace_bolt_scan`.
