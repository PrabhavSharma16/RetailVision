# RetailVision System Architecture

## 1. System Overview

RetailVision is an intelligent shelf monitoring and visual inventory analytics system designed to analyze retail shelf images using computer vision and object detection.

The system accepts a retail shelf image as input, detects visible products using a custom-trained YOLO model, performs shelf occupancy analysis, generates inventory insights, and produces an annotated visual output.

---

## 2. High-Level Architecture

```text
                    ┌─────────────────────────┐
                    │       USER INPUT        │
                    │   Retail Shelf Image    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   IMAGE PREPROCESSING   │
                    │                         │
                    │ • Image Loading         │
                    │ • Resizing              │
                    │ • Normalization         │
                    │                         │
                    │ OpenCV + NumPy          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    PRODUCT DETECTION    │
                    │                         │
                    │ Custom YOLO11 Model     │
                    │                         │
                    │ Classes:                │
                    │ • Product               │
                    │ • Price                 │
                    └────────────┬────────────┘
                                 │
                                 ▼
              ┌──────────────────┴──────────────────┐
              │                                     │
              ▼                                     ▼
   ┌─────────────────────────┐          ┌─────────────────────────┐
   │     SHELF ANALYSIS      │          │   INVENTORY ANALYTICS   │
   │                         │          │                         │
   │ • Product Counting      │          │ • Total Inventory       │
   │ • Confidence Analysis   │          │ • Product Distribution  │
   │ • Zone Analysis         │          │ • Low Stock Detection   │
   │ • Occupancy Estimation  │          │ • Inventory Status      │
   └────────────┬────────────┘          └────────────┬────────────┘
                │                                    │
                └────────────────┬───────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   VISUALIZATION MODULE │
                    │                         │
                    │ • Bounding Boxes       │
                    │ • Detection Labels     │
                    │ • Analytics Summary    │
                    │ • Shelf Status         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │         OUTPUT          │
                    │                         │
                    │ • Annotated Image      │
                    │ • Shelf Analytics      │
                    │ • Inventory Insights   │
                    └─────────────────────────┘
3. Major Components
3.1 Image Preprocessing Module

File: src/preprocessing/image_preprocessor.py

The preprocessing module prepares input images before analysis.

Responsibilities:

Load the input image.
Validate the image path.
Resize the image to the required dimensions.
Normalize pixel values.
Handle invalid or unreadable images.

Technologies:

Python
OpenCV
NumPy
3.2 Product Detection Module

File: src/detection/product_detector.py

The product detection module uses a custom-trained YOLO model to identify objects in retail shelf images.

The trained model recognizes:

Product
Price

For every detected object, the module generates:

Class ID
Class name
Confidence score
Bounding box coordinates

Technologies:

Python
Ultralytics YOLO
PyTorch
3.3 Shelf Analysis Module

File: src/analysis/shelf_analyzer.py

The shelf analysis module processes the detection results to generate shelf-level information.

Responsibilities:

Count detected objects.
Calculate average detection confidence.
Divide the image into analysis zones.
Estimate occupancy for each zone.
Identify zones with potentially low stock.

The current occupancy calculation is a computational estimate based on the detected bounding-box area within horizontal shelf zones.

3.4 Inventory Analytics Module

File: src/analytics/inventory_analyzer.py

The inventory analytics module converts object detection results into inventory-level information.

Responsibilities:

Calculate total detected inventory.
Identify unique detected classes.
Calculate product frequency.
Identify low-stock classes.
Identify dominant product classes.
Generate an overall inventory status.

Possible inventory states include:

NO INVENTORY DETECTED
RESTOCK REQUIRED
INVENTORY HEALTHY
3.5 Visualization Module

File: src/visualization/result_visualizer.py

The visualization module converts analytical results into a visual representation.

Responsibilities:

Draw detection bounding boxes.
Display class labels.
Display confidence scores.
Generate the RetailVision analytics summary panel.
Save the final annotated image.

Output:

outputs/detections/retailvision_result.jpg

3.6 Main Pipeline Module

File: src/main.py

The main module integrates all components into a single execution pipeline.

Processing sequence:

Validate input image.
Load the trained YOLO model.
Detect products.
Analyze shelf occupancy.
Generate inventory analytics.
Create the annotated visualization.
Save the final output.
Display analysis results in the terminal.
4. Data Flow
Retail Shelf Image
        │
        ▼
Image Preprocessing
        │
        ▼
YOLO Object Detection
        │
        ▼
Detection Results
        │
        ├───────────────┐
        ▼               ▼
Shelf Analysis    Inventory Analysis
        │               │
        └───────┬───────┘
                ▼
        Visualization
                │
                ▼
       Annotated Output
5. Technology Stack
Layer	Technology
Programming Language	Python
Computer Vision	OpenCV
Numerical Processing	NumPy
Object Detection	Ultralytics YOLO11
Deep Learning Framework	PyTorch
Data Processing	Pandas
Machine Learning Utilities	Scikit-learn
Image Processing	Pillow
Testing	Pytest
Version Control	Git
Repository	GitHub
6. Model Architecture

RetailVision uses a YOLO11-based object detection model that was fine-tuned using the Supermarket Shelves dataset.

The model was trained for two object classes:

Class 0 → Product
Class 1 → Price

The trained model is stored locally as:

models/retailvision_v2.pt

Model weights are excluded from the GitHub repository through .gitignore.

7. Model Evaluation

The final validation run was performed using:

Image size: 640 × 640
Validation batch size: 1
Validation images: 9

Final evaluation results:

Metric	Result
Precision	0.543
Recall	0.442
mAP@50	0.385
mAP@50-95	0.165
Product mAP@50	0.396
Price mAP@50	0.373

These measurements are used as the model evaluation results for the current implementation.

8. Non-Functional Design Considerations
Performance

The system performs object detection using a trained YOLO model and processes images through a modular pipeline.

Reliability

Input validation and error handling are implemented for missing or unreadable image files.

Maintainability

The project is divided into independent modules for preprocessing, detection, analysis, analytics, visualization, and testing.

Usability

The system provides a command-line interface with configurable model path and confidence threshold.

Scalability

The modular architecture allows additional analysis modules, product classes, and visualization features to be integrated without redesigning the complete system.

Testability

Automated tests are implemented using Pytest for preprocessing, shelf analysis, inventory analytics, and visualization components.

9. Error Handling

RetailVision performs validation at multiple stages.

Examples include:

Missing input image.
Invalid image files.
Missing model file.
Invalid image dimensions.
Empty detection results.
Invalid bounding-box data.
Invalid visualization input.

Exceptions are raised with descriptive messages to help identify the source of an error.

10. Project Workflow
START
  │
  ▼
Select Retail Shelf Image
  │
  ▼
Validate Input
  │
  ▼
Load Image
  │
  ▼
Run YOLO Detection
  │
  ▼
Extract Detection Results
  │
  ├───────────────┐
  ▼               ▼
Shelf Analysis   Inventory Analysis
  │               │
  └───────┬───────┘
          ▼
Generate Analytics
          │
          ▼
Draw Bounding Boxes
          │
          ▼
Generate Summary Panel
          │
          ▼
Save Annotated Image
          │
          ▼
         END
11. Directory Structure
RetailVision/
│
├── data/
│   └── yolo/
│       └── dataset.yaml
│
├── docs/
│   └── architecture.md
│
├── models/
│   └── retailvision_v2.pt
│
├── outputs/
│   └── detections/
│       └── retailvision_result.jpg
│
├── src/
│   ├── analysis/
│   │   └── shelf_analyzer.py
│   │
│   ├── analytics/
│   │   └── inventory_analyzer.py
│   │
│   ├── data/
│   │   └── prepare_dataset.py
│   │
│   ├── detection/
│   │   └── product_detector.py
│   │
│   ├── preprocessing/
│   │   └── image_preprocessor.py
│   │
│   ├── visualization/
│   │   └── result_visualizer.py
│   │
│   ├── config.py
│   └── main.py
│
├── tests/
│   ├── test_preprocessing.py
│   ├── test_shelf_analyzer.py
│   ├── test_inventory_analyzer.py
│   └── test_visualization.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── statement.md
12. Design Rationale

The system follows a modular architecture so that each major computer vision operation can be developed, tested, and maintained independently.

YOLO was selected as the object detection approach because the project requires localization of multiple objects within a retail shelf image.

The shelf analysis component operates on detection bounding boxes rather than directly modifying the detection model. This separates object detection from higher-level retail analytics.

The inventory analytics component similarly operates on structured detection results, allowing analytical rules to be changed without retraining the detection model.

The visualization layer is kept separate from the analytical logic so that output presentation can evolve independently.

13. Future Extensibility

Potential future improvements include:

Product-specific classification.
Barcode and OCR integration.
Real-time video monitoring.
Automated restocking alerts.
Historical inventory tracking.
Database integration.
Store-wide shelf monitoring.
Cloud deployment.
Web-based analytics dashboard.
Improved shelf-row detection.