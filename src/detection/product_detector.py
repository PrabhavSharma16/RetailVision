"""
Product detection utilities for RetailVision.
"""

from pathlib import Path

from ultralytics import YOLO


DEFAULT_MODEL = "models/retailvision_v2.pt"


class ProductDetector:
    """Detect objects/products in retail images using YOLO."""

    def __init__(self, model_path=DEFAULT_MODEL, confidence=0.25):
        self.model_path = model_path
        self.confidence = confidence
        self.model = YOLO(model_path)

    def detect(self, image_path):
        """
        Run object detection on an image.

        Returns:
            list: Detection results containing class, confidence and bounding box.
        """
        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        results = self.model.predict(
            source=str(image_path),
            conf=self.confidence,
            verbose=False
        )

        detections = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                coordinates = box.xyxy[0].tolist()

                detections.append(
                    {
                        "class_id": class_id,
                        "class_name": self.model.names[class_id],
                        "confidence": confidence,
                        "bbox": coordinates,
                    }
                )

        return detections


def detect_products(image_path, model_path=DEFAULT_MODEL, confidence=0.25):
    """Convenience function for product detection."""
    detector = ProductDetector(
        model_path=model_path,
        confidence=confidence
    )

    return detector.detect(image_path)