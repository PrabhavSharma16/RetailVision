"""
Visualization utilities for RetailVision.
"""

from pathlib import Path
import cv2


class ResultVisualizer:
    """Draw detection results and analytics on retail images."""

    def __init__(self, output_dir="outputs/detections"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def draw_detections(self, image, detections):
        """Draw bounding boxes and labels for detected objects."""

        if image is None:
            raise ValueError("Image cannot be None.")

        annotated = image.copy()

        for detection in detections:
            bbox = detection.get("bbox")
            class_name = detection.get("class_name", "Object")
            confidence = float(detection.get("confidence", 0.0))

            if not bbox or len(bbox) != 4:
                continue

            x1, y1, x2, y2 = map(int, bbox)

            cv2.rectangle(
                annotated,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = f"{class_name} {confidence:.2f}"

            cv2.putText(
                annotated,
                label,
                (x1, max(y1 - 8, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 255, 0),
                1,
                cv2.LINE_AA
            )

        return annotated

    def draw_summary_panel(
        self,
        image,
        total_products,
        average_confidence,
        occupancy=None,
        inventory_status="UNKNOWN",
        low_stock_zones=None,
    ):
        """Add a compact analytics summary panel."""

        if image is None:
            raise ValueError("Image cannot be None.")

        annotated = image.copy()

        low_stock_zones = low_stock_zones or []

        height, width = annotated.shape[:2]

        panel_height = 150
        panel_width = min(width, 520)

        # Semi-transparent panel
        overlay = annotated.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (panel_width, panel_height),
            (20, 20, 20),
            -1
        )

        annotated = cv2.addWeighted(
            overlay,
            0.82,
            annotated,
            0.18,
            0
        )

        # Title
        cv2.putText(
            annotated,
            "RETAILVISION | SHELF ANALYTICS",
            (15, 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Product count
        cv2.putText(
            annotated,
            f"Products Detected : {total_products}",
            (15, 58),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        # Confidence
        cv2.putText(
            annotated,
            f"Avg Confidence    : {average_confidence:.2%}",
            (15, 82),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        # Occupancy
        occupancy_text = "N/A"

        if occupancy is not None:
            occupancy_text = f"{occupancy:.2%}"

        cv2.putText(
            annotated,
            f"Shelf Occupancy   : {occupancy_text}",
            (15, 106),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        # Inventory status
        cv2.putText(
            annotated,
            f"Inventory Status  : {inventory_status}",
            (15, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        # Low stock zone information
        if low_stock_zones:
            zone_text = ", ".join(map(str, low_stock_zones))
        else:
            zone_text = "None"

        cv2.putText(
            annotated,
            f"Low-Stock Zones   : {zone_text}",
            (280, 58),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        return annotated

    def save_result(self, image, filename="result.jpg"):
        """Save the final visualization."""

        if image is None:
            raise ValueError("Image cannot be None.")

        output_path = self.output_dir / filename

        success = cv2.imwrite(
            str(output_path),
            image
        )

        if not success:
            raise IOError(
                f"Unable to save image: {output_path}"
            )

        return output_path


def visualize_results(
    image,
    detections,
    output_dir="outputs/detections"
):
    """Convenience function for detection visualization."""

    visualizer = ResultVisualizer(output_dir)

    annotated = visualizer.draw_detections(
        image,
        detections
    )

    return visualizer.save_result(
        annotated
    )