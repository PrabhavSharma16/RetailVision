from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Main project directories
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"


# Input / output paths
INPUT_DIR = DATA_DIR / "images"
OUTPUT_DIR = OUTPUTS_DIR / "detections"


# Model configuration
MODEL_NAME = "yolo11n.pt"

CONFIDENCE_THRESHOLD = 0.40
IOU_THRESHOLD = 0.50


# Image configuration
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]


# Create required directories if they don't exist
for directory in [
    DATA_DIR,
    MODELS_DIR,
    OUTPUTS_DIR,
    INPUT_DIR,
    OUTPUT_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)