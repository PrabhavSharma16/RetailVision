import pytest

from src.analytics.inventory_analyzer import InventoryAnalyzer


@pytest.fixture
def sample_detections():
    return [
        {
            "class_id": 0,
            "class_name": "Product",
            "confidence": 0.90,
            "bbox": [10, 10, 100, 100],
        },
        {
            "class_id": 0,
            "class_name": "Product",
            "confidence": 0.85,
            "bbox": [120, 20, 220, 120],
        },
        {
            "class_id": 0,
            "class_name": "Product",
            "confidence": 0.80,
            "bbox": [230, 30, 330, 130],
        },
        {
            "class_id": 1,
            "class_name": "Price",
            "confidence": 0.75,
            "bbox": [50, 150, 150, 180],
        },
    ]


def test_total_inventory(sample_detections):
    analyzer = InventoryAnalyzer(sample_detections)

    assert analyzer.total_inventory() == 4


def test_product_counts(sample_detections):
    analyzer = InventoryAnalyzer(sample_detections)

    counts = analyzer.product_counts()

    assert counts["Product"] == 3
    assert counts["Price"] == 1


def test_unique_products(sample_detections):
    analyzer = InventoryAnalyzer(sample_detections)

    assert analyzer.unique_products() == 2


def test_low_stock_products(sample_detections):
    analyzer = InventoryAnalyzer(sample_detections)

    low_stock = analyzer.low_stock_products(threshold=2)

    assert low_stock == {"Price": 1}


def test_dominant_products(sample_detections):
    analyzer = InventoryAnalyzer(sample_detections)

    dominant = analyzer.dominant_products(top_n=1)

    assert dominant[0] == ("Product", 3)


def test_inventory_status():
    analyzer = InventoryAnalyzer([])

    assert analyzer.inventory_status() == "NO INVENTORY DETECTED"


def test_healthy_inventory(sample_detections):
    analyzer = InventoryAnalyzer(sample_detections)

    assert (
        analyzer.inventory_status(low_stock_threshold=1)
        == "INVENTORY HEALTHY"
    )


def test_inventory_summary(sample_detections):
    analyzer = InventoryAnalyzer(sample_detections)

    summary = analyzer.inventory_summary(low_stock_threshold=2)

    assert summary["total_inventory"] == 4
    assert summary["unique_products"] == 2
    assert summary["product_counts"]["Product"] == 3
    assert summary["inventory_status"] == "RESTOCK REQUIRED"