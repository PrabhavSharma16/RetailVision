from pathlib import Path

import numpy as np
import pytest

from src.preprocessing.image_preprocessor import (
    resize_image,
    normalize_image,
)


def test_resize_image():
    image = np.zeros((100, 200, 3), dtype=np.uint8)

    resized = resize_image(
        image,
        width=640,
        height=640
    )

    assert resized.shape == (640, 640, 3)


def test_normalize_image():
    image = np.full(
        (10, 10, 3),
        255,
        dtype=np.uint8
    )

    normalized = normalize_image(image)

    assert normalized.dtype == np.float32
    assert np.allclose(normalized, 1.0)


def test_resize_rejects_none():
    with pytest.raises(ValueError):
        resize_image(None)


def test_normalize_rejects_none():
    with pytest.raises(ValueError):
        normalize_image(None)