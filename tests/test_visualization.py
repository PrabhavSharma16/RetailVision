import numpy as np
import pytest

from src.visualization.result_visualizer import ResultVisualizer


@pytest.fixture
def sample_image():
    return np.zeros((400, 600, 3), dtype=np.uint8)


@pytest.fixture
def sample_detections():
    return [
        {
            "class_id": 0,
            "class_name": "Product",
            "confidence": 0.90,
            "bbox": [50, 50, 150, 150],
        },
        {
            "class_id": 0,
            "class_name": "Product",
            "confidence": 0.85,
            "bbox": [200, 100, 300, 200],
        },
    ]


def test_draw_detections(sample_image, sample_detections):
    visualizer = ResultVisualizer()

    result = visualizer.draw_detections(
        sample_image,
        sample_detections
    )

    assert result.shape == sample_image.shape
    assert result is not sample_image


def test_draw_summary_panel(sample_image):
    visualizer = ResultVisualizer()

    result = visualizer.draw_summary_panel(
        sample_image,
        total_products=10,
        average_confidence=0.85,
        occupancy=0.70,
        inventory_status="INVENTORY HEALTHY",
        low_stock_zones=[]
    )

    assert result.shape == sample_image.shape
    assert result is not sample_image


def test_save_result(sample_image, tmp_path):
    visualizer = ResultVisualizer(
        output_dir=tmp_path
    )

    output_path = visualizer.save_result(
        sample_image,
        "test_result.jpg"
    )

    assert output_path.exists()
    assert output_path.name == "test_result.jpg"


def test_draw_detections_rejects_none():
    visualizer = ResultVisualizer()

    with pytest.raises(ValueError):
        visualizer.draw_detections(
            None,
            []
        )


def test_summary_panel_rejects_none():
    visualizer = ResultVisualizer()

    with pytest.raises(ValueError):
        visualizer.draw_summary_panel(
            None,
            total_products=0,
            average_confidence=0.0
        )