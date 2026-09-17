# RetailVision Class Diagram

## Class Structure

```mermaid
classDiagram

    class ProductDetector {
        - model_path
        - confidence
        - model
        + __init__(model_path, confidence)
        + detect(image_path)
    }

    class ShelfAnalyzer {
        - detections
        + __init__(detections)
        + set_detections(detections)
        + count_products()
        + total_products()
        + average_confidence()
        + estimate_occupancy(image_width, image_height)
        + analyze(image_width, image_height)
    }

    class InventoryAnalyzer {
        - detections
        + __init__(detections)
        + set_detections(detections)
        + product_counts()
        + total_inventory()
        + unique_products()
        + low_stock_products(threshold)
        + dominant_products(top_n)
        + inventory_status(low_stock_threshold)
        + inventory_summary(low_stock_threshold)
    }

    class ResultVisualizer {
        - output_dir
        + __init__(output_dir)
        + draw_detections(image, detections)
        + draw_summary_panel(image, total_products, average_confidence, occupancy, inventory_status, low_stock_zones)
        + save_result(image, filename)
    }

    class MainPipeline {
        + run_pipeline(image_path, model_path, confidence)
        + main()
    }

    MainPipeline --> ProductDetector : uses
    MainPipeline --> ShelfAnalyzer : uses
    MainPipeline --> InventoryAnalyzer : uses
    MainPipeline --> ResultVisualizer : uses

    ProductDetector --> ShelfAnalyzer : detection results
    ProductDetector --> InventoryAnalyzer : detection results
    ShelfAnalyzer --> ResultVisualizer : shelf analytics
    InventoryAnalyzer --> ResultVisualizer : inventory analytics
Class Responsibilities
ProductDetector

Responsible for loading the trained YOLO model and detecting objects in retail shelf images.

Input: Retail shelf image

Output: Detection records containing:

Class ID
Class name
Confidence score
Bounding-box coordinates
ShelfAnalyzer

Responsible for analyzing detected objects at the shelf level.

It calculates:

Total detections
Product/class counts
Average confidence
Zone-wise occupancy
Potential low-stock zones
InventoryAnalyzer

Responsible for converting detection results into inventory insights.

It calculates:

Total inventory
Unique detected classes
Product frequency
Low-stock products
Dominant products
Overall inventory status
ResultVisualizer

Responsible for presenting the computer vision results visually.

It provides:

Bounding boxes
Detection labels
Confidence scores
Analytics summary panel
Annotated output image
MainPipeline

The main pipeline coordinates all system modules.

The processing sequence is:

Input Image
     ↓
ProductDetector
     ↓
Detection Results
     ├───────────────┐
     ↓               ↓
ShelfAnalyzer   InventoryAnalyzer
     └───────┬───────┘
             ↓
      ResultVisualizer
             ↓
      Annotated Output
Design Principle

Each class has a focused responsibility. Detection, shelf analysis, inventory analytics, and visualization are separated into independent modules. This improves maintainability, testability, and future extensibility.