"""
Shelf analysis utilities for RetailVision.
"""

from collections import Counter


class ShelfAnalyzer:
    """Analyze detected products and generate shelf-level statistics."""

    def __init__(self, detections=None):
        self.detections = detections or []

    def set_detections(self, detections):
        """Update the detections used for analysis."""
        self.detections = detections or []

    def count_products(self):
        """Count detected objects by product/class name."""
        return Counter(
            detection["class_name"]
            for detection in self.detections
            if "class_name" in detection
        )

    def total_products(self):
        """Return the total number of detected products."""
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

    def analyze(self):
        """Generate a complete shelf analysis summary."""
        product_counts = self.count_products()

        return {
            "total_products": self.total_products(),
            "unique_products": len(product_counts),
            "product_counts": dict(product_counts),
            "average_confidence": round(self.average_confidence(), 4),
        }


def analyze_shelf(detections):
    """Convenience function for shelf analysis."""
    analyzer = ShelfAnalyzer(detections)
    return analyzer.analyze()