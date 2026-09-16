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
        """Return the count of each detected product class."""
        return Counter(
            detection["class_name"]
            for detection in self.detections
            if "class_name" in detection
        )

    def total_inventory(self):
        """Return the total number of detected products."""
        return len(self.detections)

    def unique_products(self):
        """Return the number of unique detected product classes."""
        return len(self.product_counts())

    def low_stock_products(self, threshold=2):
        """Identify product classes below the stock threshold."""
        counts = self.product_counts()

        return {
            product: count
            for product, count in counts.items()
            if count < threshold
        }

    def dominant_products(self, top_n=5):
        """Return the most frequently detected product classes."""
        return self.product_counts().most_common(top_n)

    def inventory_status(self, low_stock_threshold=2):
        """Return an overall inventory status."""
        low_stock = self.low_stock_products(low_stock_threshold)

        if self.total_inventory() == 0:
            return "NO INVENTORY DETECTED"

        if low_stock:
            return "RESTOCK REQUIRED"

        return "INVENTORY HEALTHY"

    def inventory_summary(self, low_stock_threshold=2):
        """Generate a complete inventory summary."""
        counts = self.product_counts()
        low_stock = self.low_stock_products(low_stock_threshold)

        return {
            "total_inventory": self.total_inventory(),
            "unique_products": self.unique_products(),
            "product_counts": dict(counts),
            "top_products": self.dominant_products(),
            "low_stock_products": low_stock,
            "inventory_status": self.inventory_status(
                low_stock_threshold
            ),
        }


def analyze_inventory(detections, low_stock_threshold=2):
    """Convenience function for inventory analysis."""
    analyzer = InventoryAnalyzer(detections)

    return analyzer.inventory_summary(
        low_stock_threshold=low_stock_threshold
    )