"""
Shelf analysis utilities for RetailVision.
"""

from collections import Counter


class ShelfAnalyzer:
    """Analyze detected products and estimate shelf occupancy."""

    def __init__(self, detections=None):
        self.detections = detections or []

    def set_detections(self, detections):
        """Update detections used for analysis."""
        self.detections = detections or []

    def count_products(self):
        """Count detected products by class name."""
        return Counter(
            detection["class_name"]
            for detection in self.detections
            if "class_name" in detection
        )

    def total_products(self):
        """Return total number of detected products."""
        return len(self.detections)

    def average_confidence(self):
        """Return average detection confidence."""
        if not self.detections:
            return 0.0

        confidences = [
            float(detection["confidence"])
            for detection in self.detections
            if "confidence" in detection
        ]

        if not confidences:
            return 0.0

        return sum(confidences) / len(confidences)

    def estimate_occupancy(
        self,
        image_width,
        image_height,
        empty_threshold=0.10
    ):
        """
        Estimate shelf occupancy using detected bounding boxes.

        The image is divided into horizontal shelf zones.
        A zone with low detected product coverage is marked
        as a possible empty/low-stock region.
        """

        if image_width <= 0 or image_height <= 0:
            raise ValueError("Image dimensions must be positive.")

        zone_height = image_height / 5
        zones = []

        for zone_index in range(5):
            zone_top = zone_index * zone_height
            zone_bottom = (zone_index + 1) * zone_height

            zone_area = image_width * zone_height
            occupied_area = 0.0
            product_count = 0

            for detection in self.detections:
                bbox = detection.get("bbox")

                if not bbox or len(bbox) != 4:
                    continue

                x1, y1, x2, y2 = bbox

                intersection_top = max(y1, zone_top)
                intersection_bottom = min(y2, zone_bottom)

                if intersection_bottom <= intersection_top:
                    continue

                intersection_height = intersection_bottom - intersection_top
                intersection_width = max(0, min(x2, image_width) - max(x1, 0))

                occupied_area += (
                    intersection_width * intersection_height
                )

                product_count += 1

            occupancy = min(occupied_area / zone_area, 1.0)

            zones.append(
                {
                    "zone": zone_index + 1,
                    "product_count": product_count,
                    "occupancy": round(occupancy, 4),
                    "status": (
                        "LOW_STOCK"
                        if occupancy < empty_threshold
                        else "OCCUPIED"
                    ),
                }
            )

        average_occupancy = sum(
            zone["occupancy"] for zone in zones
        ) / len(zones)

        return {
            "average_occupancy": round(average_occupancy, 4),
            "zones": zones,
            "low_stock_zones": [
                zone["zone"]
                for zone in zones
                if zone["status"] == "LOW_STOCK"
            ],
        }

    def analyze(self, image_width=None, image_height=None):
        """Generate a complete shelf analysis summary."""

        product_counts = self.count_products()

        result = {
            "total_products": self.total_products(),
            "unique_products": len(product_counts),
            "product_counts": dict(product_counts),
            "average_confidence": round(
                self.average_confidence(),
                4
            ),
        }

        if image_width and image_height:
            result["occupancy_analysis"] = self.estimate_occupancy(
                image_width,
                image_height
            )

        return result


def analyze_shelf(
    detections,
    image_width=None,
    image_height=None
):
    """Convenience function for shelf analysis."""

    analyzer = ShelfAnalyzer(detections)

    return analyzer.analyze(
        image_width=image_width,
        image_height=image_height
    )