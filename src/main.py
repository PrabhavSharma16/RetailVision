"""
Main entry point for RetailVision.

RetailVision:
Intelligent Shelf Monitoring & Visual Inventory Analytics System
"""

import argparse
from pathlib import Path

import cv2

from src.detection.product_detector import ProductDetector
from src.analysis.shelf_analyzer import ShelfAnalyzer
from src.analytics.inventory_analyzer import InventoryAnalyzer
from src.visualization.result_visualizer import ResultVisualizer


# Default trained RetailVision model
DEFAULT_MODEL = "models/retailvision_v2.pt"


def run_pipeline(
    image_path,
    model_path=DEFAULT_MODEL,
    confidence=0.50
):
    """
    Run the complete RetailVision analysis pipeline.

    Pipeline:
    Image Input
        ↓
    Product Detection
        ↓
    Shelf Analysis
        ↓
    Inventory Analytics
        ↓
    Visualization
    """

    print("\n" + "=" * 55)
    print("        RETAILVISION")
    print("  Intelligent Shelf Monitoring System")
    print("=" * 55)

    image_path = Path(image_path)

    print(f"\nInput image : {image_path}")
    print(f"Model       : {model_path}")
    print(f"Confidence  : {confidence}")

    # ---------------------------------------------------------
    # Input Validation
    # ---------------------------------------------------------

    if not image_path.exists():
        raise FileNotFoundError(
            f"Input image not found: {image_path}"
        )

    model_file = Path(model_path)

    if not model_file.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    # ---------------------------------------------------------
    # Load Image
    # ---------------------------------------------------------

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(
            f"Unable to read image: {image_path}"
        )

    image_height, image_width = image.shape[:2]

    print(
        f"Image size   : "
        f"{image_width} x {image_height}"
    )

    # ---------------------------------------------------------
    # 1. Product Detection
    # ---------------------------------------------------------

    print("\n[1/4] Detecting products...")

    detector = ProductDetector(
        model_path=model_path,
        confidence=confidence
    )

    detections = detector.detect(image_path)

    print(
        f"Detections generated: {len(detections)}"
    )

    # ---------------------------------------------------------
    # 2. Shelf Analysis
    # ---------------------------------------------------------

    print("[2/4] Analyzing shelf...")

    shelf_analyzer = ShelfAnalyzer(
        detections
    )

    shelf_summary = shelf_analyzer.analyze(
        image_width=image_width,
        image_height=image_height
    )

    # ---------------------------------------------------------
    # 3. Inventory Analytics
    # ---------------------------------------------------------

    print("[3/4] Generating inventory insights...")

    inventory_analyzer = InventoryAnalyzer(
        detections
    )

    inventory_summary = (
        inventory_analyzer.inventory_summary()
    )

    # ---------------------------------------------------------
    # 4. Visualization
    # ---------------------------------------------------------

    print("[4/4] Creating visualization...")

    visualizer = ResultVisualizer()

    # Draw detection bounding boxes
    annotated_image = visualizer.draw_detections(
        image,
        detections
    )

    # Get occupancy analysis
    occupancy_analysis = shelf_summary.get(
        "occupancy_analysis",
        {}
    )

    average_occupancy = occupancy_analysis.get(
        "average_occupancy"
    )

    low_stock_zones = occupancy_analysis.get(
        "low_stock_zones",
        []
    )

    # Add analytics dashboard
    annotated_image = visualizer.draw_summary_panel(
        annotated_image,
        total_products=shelf_summary[
            "total_products"
        ],
        average_confidence=shelf_summary[
            "average_confidence"
        ],
        occupancy=average_occupancy,
        inventory_status=inventory_summary[
            "inventory_status"
        ],
        low_stock_zones=low_stock_zones
    )

    # Save final result
    output_path = visualizer.save_result(
        annotated_image,
        "retailvision_result.jpg"
    )

    # ---------------------------------------------------------
    # Console Results
    # ---------------------------------------------------------

    print("\n" + "=" * 55)
    print("             ANALYSIS RESULTS")
    print("=" * 55)

    print(
        f"\nTotal detections       : "
        f"{shelf_summary['total_products']}"
    )

    print(
        f"Unique classes         : "
        f"{shelf_summary['unique_products']}"
    )

    print(
        f"Average confidence     : "
        f"{shelf_summary['average_confidence']:.2%}"
    )

    # ---------------------------------------------------------
    # Shelf Occupancy Results
    # ---------------------------------------------------------

    if average_occupancy is not None:

        print(
            f"Average shelf occupancy: "
            f"{average_occupancy:.2%}"
        )

        print(
            f"Low-stock zones        : "
            f"{low_stock_zones}"
        )

        print("\nZone Analysis:")

        for zone in occupancy_analysis.get(
            "zones",
            []
        ):
            print(
                f"  Zone {zone['zone']} → "
                f"{zone['occupancy']:.2%} occupied | "
                f"{zone['status']}"
            )

    # ---------------------------------------------------------
    # Inventory Results
    # ---------------------------------------------------------

    print("\nInventory Summary:")

    print(
        f"Total inventory        : "
        f"{inventory_summary['total_inventory']}"
    )

    print(
        f"Unique products        : "
        f"{inventory_summary['unique_products']}"
    )

    print(
        f"Low-stock products     : "
        f"{inventory_summary['low_stock_products']}"
    )

    print(
        f"Inventory status       : "
        f"{inventory_summary['inventory_status']}"
    )

    print(
        f"\nResult saved to        : "
        f"{output_path}"
    )

    print("\n" + "=" * 55)
    print("       PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 55)

    # ---------------------------------------------------------
    # Return Complete Results
    # ---------------------------------------------------------

    return {
        "input_image": str(image_path),
        "model": str(model_path),
        "confidence_threshold": confidence,
        "detections": detections,
        "shelf_analysis": shelf_summary,
        "inventory_analysis": inventory_summary,
        "output_path": str(output_path),
    }


def main():
    """Command-line interface for RetailVision."""

    parser = argparse.ArgumentParser(
        description=(
            "RetailVision - Intelligent Shelf "
            "Monitoring & Visual Inventory Analytics System"
        )
    )

    parser.add_argument(
        "image",
        help="Path to the retail shelf image"
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=(
            "Path to the trained YOLO model "
            "(default: models/retailvision_v2.pt)"
        )
    )

    parser.add_argument(
        "--confidence",
        type=float,
        default=0.50,
        help=(
            "Minimum detection confidence "
            "(default: 0.50)"
        )
    )

    args = parser.parse_args()

    run_pipeline(
        image_path=args.image,
        model_path=args.model,
        confidence=args.confidence
    )


if __name__ == "__main__":
    main()