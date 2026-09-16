"""
Inventory analysis utilities for RetailVision.
"""

from collections import Counter


class InventoryAnalyzer:
    """Analyze product detections for inventory insights."""

    def __init__(self, detections=None):
        self.detections = detections or []

    def set_detections(self, detections):
        """Update the detections used for inventory analysis."""
        self.detections = detections or []

    def product_counts(self):
        """Return the count of each detected product."""
        return Counter(
            detection["class_name"]
            for detection in self.detections
            if "class_name" in detection
        )

    def total_inventory(self):
        """Return the total number of detected products."""
        return len(self.detections)

    def unique_products(self):
        """Return the number of unique product types."""
        return len(self.product_counts())

    def low_stock_products(self, threshold=2):
        """Identify products whose detected quantity is below the threshold."""
        counts = self.product_counts()

        return {
            product: count
            for product, count in counts.items()
            if count < threshold
        }

    def inventory_summary(self):
        """Generate an inventory summary."""
        counts = self.product_counts()

        return {
            "total_inventory": self.total_inventory(),
            "unique_products": self.unique_products(),
            "product_counts": dict(counts),
            "low_stock_products": self.low_stock_products(),
        }


def analyze_inventory(detections):
    """Convenience function for inventory analysis."""
    analyzer = InventoryAnalyzer(detections)
    return analyzer.inventory_summary()