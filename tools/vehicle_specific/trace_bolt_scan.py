"""Trace the lower edge of zikeji's 2023 Bolt scan without AI geometry changes.

The pixel regions below are specific to the original 5100 x 6600 scan. The
card's long dimension supplies scale; the housing supplies rotation. Only the
visible lower edge is traced, not the blurred interior or mirror opening.
"""

from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
VEHICLE = ROOT / "vehicles/2023_chevy_bolt"


def card_scale(gray):
    edges = []
    for lower, upper, xs, last in (
        (1750, 2050, range(2250, 3200, 10), False),
        (3700, 4000, range(2150, 3150, 10), True),
    ):
        samples = []
        for x in xs:
            hits = np.flatnonzero(gray[lower:upper, x] > 190)
            if not len(hits):
                raise ValueError("Scale-card edge not found in the expected region")
            samples.append((x, lower + hits[-1 if last else 0]))
        samples = np.asarray(samples)
        slope, intercept = np.polyfit(samples[:, 0], samples[:, 1], 1)
        residual = np.max(abs(samples[:, 1] - (slope * samples[:, 0] + intercept)))
        if residual > 8:
            raise ValueError("Scale-card edge is not sufficiently straight")
        edges.append((slope, intercept))
    top, bottom = edges
    slope = (top[0] + bottom[0]) / 2
    # Distance between the short edges, normal to their common direction.
    length_px = ((bottom[0] - top[0]) * 2700 + bottom[1] - top[1]) / np.hypot(1, slope)
    return length_px / 85.60


def lower_edge(gray, pixels_per_mm):
    samples = []
    for x in range(400, 4950, 5):
        hits = np.flatnonzero(gray[4700:5650, x] < 80)
        if len(hits):
            samples.append((x, 4700 + hits[-1]))
    points = np.asarray(samples, dtype=float)
    if len(points) < 800 or np.max(np.diff(points[:, 0])) > 5:
        raise ValueError("Housing lower edge is missing or discontinuous")
    # Remove scanner placement tilt using the broad lower edge, not the card:
    # the card and housing were placed independently on the scanner.
    middle = points[(points[:, 0] >= 1600) & (points[:, 0] <= 3900)]
    slope = np.polyfit(middle[:, 0], middle[:, 1], 1)[0]
    angle = np.arctan(slope)
    c, s = np.cos(angle), np.sin(angle)
    rotated = points @ np.array([[c, -s], [s, c]])
    rotated[:, 0] -= (rotated[:, 0].min() + rotated[:, 0].max()) / 2
    rotated[:, 1] -= rotated[:, 1].max()
    mm = rotated / pixels_per_mm
    simplified = cv2.approxPolyDP(mm.astype(np.float32), 0.15, False)[:, 0, :]
    return simplified, np.degrees(angle)


def main():
    gray = cv2.imread(str(VEHICLE / "raw/scan.png"), cv2.IMREAD_GRAYSCALE)
    if gray is None or gray.shape != (6600, 5100):
        raise ValueError("Expected the original 5100 x 6600 Bolt scan")
    ppm = card_scale(gray)
    points, angle = lower_edge(gray, ppm)
    half_width = max(abs(points[:, 0])) + 5
    path = "M " + " L ".join(f"{x:.4f},{y:.4f}" for x, y in points)
    out = VEHICLE / "gen/offsets.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{2 * half_width:.4f}mm" height="20mm" '
        f'viewBox="{-half_width:.4f} -15 {2 * half_width:.4f} 20">\n'
        f'  <path d="{path}" fill="none" stroke="red" '
        'stroke-width="0.353" stroke-dasharray="4,4"/>\n'
        '  <line x1="0" y1="-15" x2="0" y2="5" stroke="red" '
        'stroke-width="1" stroke-dasharray="10,4,2,4"/>\n</svg>\n'
    )
    print(f"Card scale: {ppm:.4f} px/mm; housing tilt: {angle:.3f} degrees")
    print(f"Traced width: {np.ptp(points[:, 0]):.2f} mm; saved {out}")


if __name__ == "__main__":
    main()
