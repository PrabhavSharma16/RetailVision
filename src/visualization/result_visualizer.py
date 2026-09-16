"""
Visualization utilities for RetailVision.
"""

from pathlib import Path

import cv2


class ResultVisualizer:
    """Draw detection results and save annotated images."""

    def __init__(self, output_dir="outputs/detections"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def draw_detections(self, image, detections):
        """
        Draw bounding boxes, labels and confidence scores.

        Args:
            image: OpenCV image in BGR format.
            detections: List of detection dictionaries.

        Returns:
            Annotated OpenCV image.
        """
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
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        return annotated

    def save_result(self, image, filename="result.jpg"):
        """Save an annotated image to the output directory."""
        if image is None:
            raise ValueError("Image cannot be None.")

        output_path = self.output_dir / filename

        success = cv2.imwrite(str(output_path), image)

        if not success:
            raise IOError(f"Unable to save image: {output_path}")

        return output_path


def visualize_results(image, detections, output_dir="outputs/detections"):
    """Convenience function for drawing and saving detection results."""
    visualizer = ResultVisualizer(output_dir)

    annotated = visualizer.draw_detections(image, detections)

    return visualizer.save_result(annotated)