"""
RetailVision - Main Pipeline

Coordinates image validation, preprocessing, product detection,
shelf analysis, inventory analytics, and result visualization.
"""

import argparse
from pathlib import Path

import cv2

from src.preprocessing.image_preprocessor import load_image, resize_image
from src.detection.product_detector import ProductDetector
from src.analysis.shelf_analyzer import ShelfAnalyzer
from src.analytics.inventory_analyzer import InventoryAnalyzer
from src.visualization.result_visualizer import ResultVisualizer


DEFAULT_MODEL = "models/retailvision_v2.pt"
DEFAULT_OUTPUT_DIR = "outputs/detections"


def run_pipeline(
    image_path,
    model_path=DEFAULT_MODEL,
    confidence=0.50,
    output_dir=DEFAULT_OUTPUT_DIR,
):
    """
    Run the complete RetailVision analysis pipeline.

    Parameters
    ----------
    image_path : str
        Path to the retail shelf image.
    model_path : str
        Path to the trained YOLO model.
    confidence : float
        Minimum confidence threshold for detections.
    output_dir : str
        Directory for generated output images.

    Returns
    -------
    dict
        Complete analysis result.
    """

    image_path = Path(image_path)
    model_path = Path(model_path)

    # ---------------------------------------------------------
    # 1. Validate input image
    # ---------------------------------------------------------
    if not image_path.exists():
        raise FileNotFoundError(f"Input image not found: {image_path}")

    # ---------------------------------------------------------
    # 2. Validate trained model
    # ---------------------------------------------------------
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    if not 0.0 <= confidence <= 1.0:
        raise ValueError("Confidence threshold must be between 0.0 and 1.0.")

    # ---------------------------------------------------------
    # 3. Load image
    # ---------------------------------------------------------
    image = load_image(image_path)

    original_height, original_width = image.shape[:2]

    # ---------------------------------------------------------
    # 4. Image preprocessing
    #
    # The preprocessing module validates that the image can be
    # resized successfully before the detection stage.
    #
    # The original image is still supplied to YOLO because
    # Ultralytics performs its own inference preprocessing.
    # ---------------------------------------------------------
    processed_image = resize_image(
        image,
        width=640,
        height=640,
    )

    if processed_image is None or processed_image.size == 0:
        raise ValueError("Image preprocessing failed.")

    # ---------------------------------------------------------
    # 5. Product detection
    # ---------------------------------------------------------
    detector = ProductDetector(
        model_path=str(model_path),
        confidence=confidence,
    )

    detections = detector.detect(image_path)

    # ---------------------------------------------------------
    # 6. Shelf analysis
    # ---------------------------------------------------------
    shelf_analyzer = ShelfAnalyzer(detections)

    shelf_analysis = shelf_analyzer.analyze(
        image_width=original_width,
        image_height=original_height,
    )

    # ---------------------------------------------------------
    # 7. Inventory analysis
    # ---------------------------------------------------------
    inventory_analyzer = InventoryAnalyzer(detections)

    inventory_summary = inventory_analyzer.inventory_summary(
        low_stock_threshold=2
    )

    # ---------------------------------------------------------
    # 8. Extract analytics values
    # ---------------------------------------------------------
    occupancy_analysis = shelf_analysis.get(
        "occupancy_analysis",
        {},
    )

    average_occupancy = occupancy_analysis.get(
        "average_occupancy"
    )

    low_stock_zones = occupancy_analysis.get(
        "low_stock_zones",
        [],
    )

    inventory_status = inventory_summary.get(
        "inventory_status",
        "UNKNOWN",
    )

    # ---------------------------------------------------------
    # 9. Visualize detection results
    # ---------------------------------------------------------
    visualizer = ResultVisualizer(
        output_dir=output_dir
    )

    annotated_image = visualizer.draw_detections(
        image,
        detections,
    )

    # ---------------------------------------------------------
    # 10. Add analytics summary panel
    # ---------------------------------------------------------
    annotated_image = visualizer.draw_summary_panel(
        annotated_image,
        total_products=shelf_analysis["total_products"],
        average_confidence=shelf_analysis["average_confidence"],
        occupancy=average_occupancy,
        inventory_status=inventory_status,
        low_stock_zones=low_stock_zones,
    )

    # ---------------------------------------------------------
    # 11. Save final result
    # ---------------------------------------------------------
    output_path = visualizer.save_result(
        annotated_image,
        filename="retailvision_result.jpg",
    )

    # ---------------------------------------------------------
    # 12. Console output
    # ---------------------------------------------------------
    print("\n" + "=" * 60)
    print("RETAILVISION - ANALYSIS COMPLETE")
    print("=" * 60)

    print(f"Input image       : {image_path}")
    print(f"Image dimensions  : {original_width} x {original_height}")
    print(f"Model             : {model_path}")
    print(f"Confidence        : {confidence:.2f}")

    print("\n--- Detection Summary ---")
    print(f"Products detected : {shelf_analysis['total_products']}")
    print(
        f"Average confidence: "
        f"{shelf_analysis['average_confidence']:.4f}"
    )

    print("\n--- Shelf Analysis ---")

    if average_occupancy is not None:
        print(
            f"Average occupancy : "
            f"{average_occupancy:.4f}"
        )

    print(f"Low-stock zones   : {low_stock_zones}")

    print("\n--- Inventory Summary ---")
    print(
        f"Total inventory   : "
        f"{inventory_summary['total_inventory']}"
    )
    print(
        f"Unique products   : "
        f"{inventory_summary['unique_products']}"
    )
    print(
        f"Low-stock products: "
        f"{inventory_summary['low_stock_products']}"
    )
    print(
        f"Inventory status  : "
        f"{inventory_status}"
    )

    print("\n--- Output ---")
    print(f"Result saved to   : {output_path}")

    print("=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    # ---------------------------------------------------------
    # 13. Return structured result
    # ---------------------------------------------------------
    return {
        "input_image": str(image_path),
        "model": str(model_path),
        "confidence": confidence,
        "image_width": original_width,
        "image_height": original_height,
        "detections": detections,
        "shelf_analysis": shelf_analysis,
        "inventory_summary": inventory_summary,
        "output_path": str(output_path),
    }


def main():
    """Command-line entry point for RetailVision."""

    parser = argparse.ArgumentParser(
        description=(
            "RetailVision - Intelligent Shelf Monitoring "
            "and Visual Inventory Analytics System"
        )
    )

    parser.add_argument(
        "--image",
        required=True,
        help="Path to the retail shelf image.",
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Path to the trained YOLO model.",
    )

    parser.add_argument(
        "--confidence",
        type=float,
        default=0.50,
        help="Detection confidence threshold (0.0 to 1.0).",
    )

    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where the annotated result will be saved.",
    )

    args = parser.parse_args()

    run_pipeline(
        image_path=args.image,
        model_path=args.model,
        confidence=args.confidence,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()