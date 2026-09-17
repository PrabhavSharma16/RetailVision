import pytest

from src.analysis.shelf_analyzer import ShelfAnalyzer


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
            "confidence": 0.80,
            "bbox": [120, 20, 220, 120],
        },
        {
            "class_id": 1,
            "class_name": "Price",
            "confidence": 0.75,
            "bbox": [50, 150, 150, 180],
        },
    ]


def test_total_products(sample_detections):
    analyzer = ShelfAnalyzer(sample_detections)
    assert analyzer.total_products() == 3


def test_product_counts(sample_detections):
    analyzer = ShelfAnalyzer(sample_detections)

    counts = analyzer.count_products()

    assert counts["Product"] == 2
    assert counts["Price"] == 1


def test_average_confidence(sample_detections):
    analyzer = ShelfAnalyzer(sample_detections)

    average = analyzer.average_confidence()

    assert round(average, 2) == 0.82


def test_empty_detections():
    analyzer = ShelfAnalyzer([])

    assert analyzer.total_products() == 0
    assert analyzer.average_confidence() == 0.0


def test_occupancy_analysis(sample_detections):
    analyzer = ShelfAnalyzer(sample_detections)

    result = analyzer.estimate_occupancy(
        image_width=640,
        image_height=640
    )

    assert "average_occupancy" in result
    assert "zones" in result
    assert len(result["zones"]) == 5


def test_invalid_dimensions(sample_detections):
    analyzer = ShelfAnalyzer(sample_detections)

    with pytest.raises(ValueError):
        analyzer.estimate_occupancy(
            image_width=0,
            image_height=640
        )