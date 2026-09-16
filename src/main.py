"""
Main entry point for RetailVision.
"""

import argparse

import cv2

from src.detection.product_detector import ProductDetector
from src.analysis.shelf_analyzer import ShelfAnalyzer
from src.analytics.inventory_analyzer import InventoryAnalyzer
from src.visualization.result_visualizer import ResultVisualizer


def run_pipeline(image_path, model_path="yolo11n.pt", confidence=0.25):
    """
    Run the complete RetailVision analysis pipeline.
    """

    print("\n=== RetailVision ===")
    print(f"Input image: {image_path}")

    # Step 1: Detect products
    print("\n[1/4] Detecting products...")
    detector = ProductDetector(
        model_path=model_path,
        confidence=confidence
    )

    detections = detector.detect(image_path)

    # Step 2: Shelf analysis
    print("[2/4] Analyzing shelf...")
    shelf_analyzer = ShelfAnalyzer(detections)
    shelf_summary = shelf_analyzer.analyze()

    # Step 3: Inventory analysis
    print("[3/4] Generating inventory insights...")
    inventory_analyzer = InventoryAnalyzer(detections)
    inventory_summary = inventory_analyzer.inventory_summary()

    # Step 4: Visualization
    print("[4/4] Creating visualization...")

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")

    visualizer = ResultVisualizer()
    annotated_image = visualizer.draw_detections(
        image,
        detections
    )

    output_path = visualizer.save_result(
        annotated_image,
        "retailvision_result.jpg"
    )

    # Display results
    print("\n=== Analysis Results ===")
    print(f"Total products: {shelf_summary['total_products']}")
    print(f"Unique product classes: {shelf_summary['unique_products']}")
    print(
        f"Average confidence: "
        f"{shelf_summary['average_confidence']}"
    )

    print("\nInventory Summary:")
    print(f"Total inventory: {inventory_summary['total_inventory']}")
    print(f"Low-stock products: {inventory_summary['low_stock_products']}")

    print(f"\nResult saved to: {output_path}")

    return {
        "detections": detections,
        "shelf_analysis": shelf_summary,
        "inventory_analysis": inventory_summary,
        "output_path": str(output_path),
    }


def main():
    """Command-line entry point."""

    parser = argparse.ArgumentParser(
        description="RetailVision - Intelligent Shelf Monitoring System"
    )

    parser.add_argument(
        "image",
        help="Path to the retail shelf image"
    )

    parser.add_argument(
        "--model",
        default="yolo11n.pt",
        help="Path to YOLO model"
    )

    parser.add_argument(
        "--confidence",
        type=float,
        default=0.25,
        help="Detection confidence threshold"
    )

    args = parser.parse_args()

    run_pipeline(
        image_path=args.image,
        model_path=args.model,
        confidence=args.confidence
    )


if __name__ == "__main__":
    main()