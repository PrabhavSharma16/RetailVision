# RetailVision Sequence Diagram

## System Processing Sequence

```mermaid
sequenceDiagram
    actor User
    participant Main as Main Pipeline
    participant Detector as Product Detector
    participant Shelf as Shelf Analyzer
    participant Inventory as Inventory Analyzer
    participant Visualizer as Result Visualizer
    participant File as Output File

    User->>Main: Provide shelf image
    Main->>Main: Validate image and model path
    Main->>Detector: Load image and run detection
    Detector-->>Main: Return detection results

    Main->>Shelf: Send detections + image dimensions
    Shelf->>Shelf: Count products
    Shelf->>Shelf: Calculate confidence
    Shelf->>Shelf: Analyze shelf occupancy
    Shelf-->>Main: Return shelf analytics

    Main->>Inventory: Send detection results
    Inventory->>Inventory: Calculate product counts
    Inventory->>Inventory: Identify low-stock products
    Inventory->>Inventory: Determine inventory status
    Inventory-->>Main: Return inventory summary

    Main->>Visualizer: Send image + detections + analytics
    Visualizer->>Visualizer: Draw bounding boxes
    Visualizer->>Visualizer: Draw analytics summary
    Visualizer->>File: Save annotated result
    File-->>Visualizer: Confirm output saved
    Visualizer-->>Main: Return output path

    Main-->>User: Display analysis results
Sequence Description

The sequence begins when the User provides a retail shelf image to the main RetailVision pipeline.

The Main Pipeline validates the input image and trained model path.
The Product Detector loads the trained YOLO model and performs object detection.
Detection results containing class names, confidence scores, and bounding boxes are returned to the Main Pipeline.
The Shelf Analyzer receives the detections and image dimensions.
Shelf occupancy, product count, confidence, and low-stock zones are calculated.
The Inventory Analyzer processes the detection results to generate inventory statistics and determine the inventory status.
The Result Visualizer receives the original image, detections, and analytical results.
Bounding boxes and an analytics summary panel are added to the image.
The annotated image is saved to the output directory.
The Main Pipeline returns the final result and output location to the User.
Overall Flow
User
  ↓
Input Shelf Image
  ↓
Main Pipeline
  ↓
Product Detection
  ↓
Detection Results
  ├──────────────→ Shelf Analysis
  │                    ↓
  │              Occupancy Analysis
  │
  └──────────────→ Inventory Analysis
                       ↓
                Inventory Insights
                       ↓
              Result Visualization
                       ↓
             Annotated Output Image
                       ↓
                      User
Purpose

The sequence diagram demonstrates the interaction between the major RetailVision modules during a complete shelf-monitoring operation. It shows how detection results move through shelf analysis, inventory analytics, and visualization before the final annotated output is generated.