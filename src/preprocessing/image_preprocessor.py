"""
Image preprocessing utilities for RetailVision.
"""

from pathlib import Path

import cv2
import numpy as np


def load_image(image_path):
    """
    Load an image from the given path.

    Returns:
        numpy.ndarray: Loaded image in BGR format.

    Raises:
        FileNotFoundError: If the image does not exist or cannot be read.
    """
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")

    return image


def resize_image(image, width=640, height=640):
    """
    Resize an image to the specified dimensions.
    """
    if image is None:
        raise ValueError("Image cannot be None.")

    return cv2.resize(image, (width, height))


def normalize_image(image):
    """
    Normalize image pixel values from [0, 255] to [0, 1].
    """
    if image is None:
        raise ValueError("Image cannot be None.")

    return image.astype(np.float32) / 255.0


def preprocess_image(image_path, width=640, height=640):
    """
    Complete preprocessing pipeline:
    1. Load image
    2. Resize image
    3. Normalize pixel values
    """
    image = load_image(image_path)
    image = resize_image(image, width, height)
    image = normalize_image(image)

    return image