"""Regression checks for the submitted scan's scale and lower-edge orientation."""

import unittest

import cv2
import numpy as np

from tools.vehicle_specific.trace_bolt_scan import VEHICLE, card_scale, lower_edge


class BoltTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gray = cv2.imread(str(VEHICLE / "raw/scan.png"), cv2.IMREAD_GRAYSCALE)

    def test_scale_agrees_with_independently_measured_card_length(self):
        # The card's short edges are about 2024 pixels apart in the original.
        self.assertAlmostEqual(card_scale(self.gray) * 85.60, 2024, delta=3)

    def test_lower_edge_keeps_rounded_corners_above_the_center(self):
        points, angle = lower_edge(self.gray, card_scale(self.gray))
        self.assertTrue(np.all(np.diff(points[:, 0]) > 0))
        self.assertAlmostEqual(np.ptp(points[:, 0]), 190, delta=1)
        self.assertLess(points[0, 1], -20)
        self.assertLess(points[-1, 1], -20)
        middle = points[abs(points[:, 0]) < 50, 1]
        self.assertGreater(len(middle), 0)
        self.assertTrue(np.all(middle > -1.5))
        self.assertLess(abs(angle), 2)

    def test_missing_reference_card_fails_instead_of_assuming_pixel_scale(self):
        with self.assertRaisesRegex(ValueError, "Scale-card edge not found"):
            card_scale(np.zeros_like(self.gray))

    def test_missing_housing_edge_fails(self):
        with self.assertRaisesRegex(ValueError, "missing or discontinuous"):
            lower_edge(np.full_like(self.gray, 255), 24)


if __name__ == "__main__":
    unittest.main()
