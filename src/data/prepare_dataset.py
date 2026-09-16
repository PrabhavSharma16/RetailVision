"""
Prepare the Supermarket Shelves dataset for YOLO training.
"""

import json
import random
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / "data"

OUTPUT_ROOT = DATA_ROOT / "yolo"

TRAIN_RATIO = 0.8
RANDOM_SEED = 42

CLASS_MAP = {
    "Product": 0,
    "Price": 1,
}


def find_dataset():
    """Find the extracted dataset containing images and annotations."""

    for annotations_dir in DATA_ROOT.rglob("annotations"):
        images_dir = annotations_dir.parent / "images"

        if images_dir.exists() and images_dir.is_dir():
            return images_dir, annotations_dir

    raise FileNotFoundError(
        "Could not find dataset images/annotations folders inside data/"
    )


def convert_box(points, image_width, image_height):
    """Convert two corner points into YOLO format."""

    x1, y1 = points[0]
    x2, y2 = points[1]

    x_min = min(x1, x2)
    y_min = min(y1, y2)
    x_max = max(x1, x2)
    y_max = max(y1, y2)

    box_width = x_max - x_min
    box_height = y_max - y_min

    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2

    return (
        center_x / image_width,
        center_y / image_height,
        box_width / image_width,
        box_height / image_height,
    )


def process_annotation(annotation_path, label_path):
    """Convert one JSON annotation into a YOLO label file."""

    with open(annotation_path, "r", encoding="utf-8") as file:
        annotation = json.load(file)

    image_width = annotation["size"]["width"]
    image_height = annotation["size"]["height"]

    yolo_lines = []

    for obj in annotation.get("objects", []):
        class_title = obj.get("classTitle")

        if class_title not in CLASS_MAP:
            continue

        points = obj.get("points", {}).get("exterior", [])

        if len(points) != 2:
            continue

        class_id = CLASS_MAP[class_title]

        x_center, y_center, width, height = convert_box(
            points,
            image_width,
            image_height,
        )

        yolo_lines.append(
            f"{class_id} "
            f"{x_center:.6f} "
            f"{y_center:.6f} "
            f"{width:.6f} "
            f"{height:.6f}"
        )

    label_path.parent.mkdir(parents=True, exist_ok=True)

    with open(label_path, "w", encoding="utf-8") as file:
        file.write("\n".join(yolo_lines))


def main():
    """Prepare the complete dataset."""

    print("=== RetailVision Dataset Preparation ===")

    images_dir, annotations_dir = find_dataset()

    print(f"Images found in: {images_dir}")
    print(f"Annotations found in: {annotations_dir}")

    image_files = sorted(
        [
            path
            for path in images_dir.iterdir()
            if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
        ]
    )

    if not image_files:
        raise FileNotFoundError("No images found in dataset.")

    random.seed(RANDOM_SEED)
    random.shuffle(image_files)

    split_index = int(len(image_files) * TRAIN_RATIO)

    train_images = image_files[:split_index]
    val_images = image_files[split_index:]

    print(f"Total images: {len(image_files)}")
    print(f"Training images: {len(train_images)}")
    print(f"Validation images: {len(val_images)}")

    for split, images in [
        ("train", train_images),
        ("val", val_images),
    ]:
        image_output = OUTPUT_ROOT / "images" / split
        label_output = OUTPUT_ROOT / "labels" / split

        image_output.mkdir(parents=True, exist_ok=True)
        label_output.mkdir(parents=True, exist_ok=True)

        for image_path in images:
            annotation_path = annotations_dir / f"{image_path.name}.json"

            if not annotation_path.exists():
                print(f"Warning: annotation missing for {image_path.name}")
                continue

            shutil.copy2(
                image_path,
                image_output / image_path.name,
            )

            label_path = label_output / f"{image_path.stem}.txt"

            process_annotation(
                annotation_path,
                label_path,
            )

    print("\nDataset preparation completed.")
    print(f"YOLO dataset created at: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()