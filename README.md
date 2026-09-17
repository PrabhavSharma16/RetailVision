# RetailVision — Intelligent Shelf Monitoring & Visual Inventory Analytics System

## 1. Project Overview

RetailVision is a computer vision based shelf-monitoring system designed to analyze retail shelf images and generate visual inventory insights.

The system uses a trained YOLO object-detection model to identify products and price-related objects in shelf images. The detected objects are then processed to calculate shelf occupancy, product counts, inventory statistics, and potential low-stock conditions.

The final output is an annotated shelf image containing detection bounding boxes and an analytics summary.

---

## 2. Problem Statement

Retail stores need efficient methods to monitor shelf conditions and identify inventory-related issues.

Manual shelf inspection can be time-consuming and may make it difficult to consistently measure product presence and shelf occupancy.

RetailVision addresses this problem by using computer vision to automatically analyze shelf images and provide structured visual inventory information.

---

## 3. Objectives

The main objectives of RetailVision are:

- Detect products in retail shelf images.
- Calculate the number of detected products.
- Analyze shelf occupancy using image regions.
- Identify potential low-stock shelf zones.
- Generate inventory statistics.
- Visualize detection and analytics results.
- Provide a modular and testable computer vision pipeline.

---

## 4. Key Features

### Computer Vision

- YOLO-based object detection
- Product and price-object detection
- Bounding-box visualization
- Confidence-score reporting

### Shelf Analytics

- Product counting
- Zone-wise shelf occupancy
- Average detection confidence
- Low-stock zone identification

### Inventory Analytics

- Total inventory count
- Unique detected classes
- Product frequency analysis
- Low-stock product detection
- Inventory status generation

### Visualization

- Annotated detection image
- Detection labels and confidence scores
- Shelf analytics summary panel
- Inventory status display

### Software Engineering

- Modular architecture
- Automated testing with Pytest
- Input validation
- Error handling
- Git-based version control
- Structured documentation

---

## 5. System Workflow

```text
Retail Shelf Image
        ↓
Image Preprocessing
        ↓
YOLO Product Detection
        ↓
Detection Results
        ↓
┌───────────────────────┐
│                       │
↓                       ↓
Shelf Analysis      Inventory Analysis
│                       │
↓                       ↓
Occupancy Analysis   Inventory Insights
└───────────┬───────────┘
            ↓
     Result Visualization
            ↓
   Annotated Output Image
6. System Architecture

RetailVision follows a modular component-based architecture.

User / CLI
    ↓
Main Pipeline
    ↓
Image Preprocessing
    ↓
Product Detection
    ↓
Detection Results
    ├──────────────→ Shelf Analyzer
    │                      ↓
    │                Shelf Occupancy
    │
    └──────────────→ Inventory Analyzer
                           ↓
                    Inventory Insights
                           ↓
                  Result Visualization
                           ↓
                    Output Image

Detailed architecture and UML documentation are available in the docs/ directory.

7. Major Modules
Module	Responsibility
Image Preprocessing	Image loading, resizing and normalization
Product Detection	YOLO-based object detection
Shelf Analysis	Product counting and shelf occupancy
Inventory Analytics	Inventory statistics and stock status
Result Visualization	Bounding boxes and analytics panel
Main Pipeline	Coordinates complete system execution
Configuration	Stores reusable system parameters
8. Technology Stack
Technology	Purpose
Python	Core programming language
YOLO / Ultralytics	Object detection
OpenCV	Image processing and visualization
NumPy	Numerical operations
Pandas	Data analysis support
Matplotlib	Analytical visualization support
Scikit-learn	Machine-learning utilities
Pillow	Image handling
PyYAML	Configuration/data support
Pytest	Automated testing
Git & GitHub	Version control
9. Dataset

The project uses a supermarket shelf image dataset containing:

45 total images
36 training images
9 validation images
11,743 annotated bounding boxes
2 classes
Product
Price

The original annotations were converted into YOLO-compatible format using the dataset preparation module.

Raw dataset files are excluded from Git tracking because of their size and repository-management considerations.

10. Model

RetailVision uses a custom-trained YOLO model based on the YOLO11 nano architecture.

The trained model used by the final pipeline is:

models/retailvision_v2.pt

The model weights are intentionally excluded from Git tracking because of their size.

11. Model Validation Results

The final trained model was evaluated on the validation dataset.

Metric	Result
Precision	0.543
Recall	0.442
mAP@50	0.385
mAP@50-95	0.165
Per-Class mAP@50
Class	mAP@50
Product	0.396
Price	0.373

These values represent the validation performance obtained during project testing.

12. Installation
Clone the Repository
git clone https://github.com/PrabhavSharma16/RetailVision.git
cd RetailVision
Create Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
13. Model Setup

Place the trained model file inside:

models/

Expected model path:

models/retailvision_v2.pt

The model file is not included in the Git repository because of its file size.

14. Running the Project

Place an input shelf image in the appropriate input location.

Then run:

python -m src.main --image "path\to\image.jpg" --model "models\retailvision_v2.pt" --confidence 0.50

Example:

python -m src.main --image "data\input\001.jpg" --model "models\retailvision_v2.pt" --confidence 0.50

The pipeline performs:

Input validation
Object detection
Shelf analysis
Inventory analysis
Result visualization
Output generation
15. Output

The annotated result is generated in:

outputs/detections/retailvision_result.jpg

The output contains:

Product bounding boxes
Class labels
Detection confidence
Number of detected products
Average confidence
Shelf occupancy
Inventory status
Low-stock zone information
16. Testing

RetailVision includes automated unit tests using Pytest.

Run all tests with:

python -m pytest -q

Final test result:

23 passed in 1.54s
Testing Coverage

The automated tests cover:

Image preprocessing
Shelf analysis
Inventory analytics
Visualization
Input validation
Error handling

All 23 automated tests passed successfully during final validation.

17. Error Handling

The system validates common failure conditions including:

Missing image files
Unreadable images
Invalid image inputs
Invalid image dimensions
Missing model files
Invalid visualization inputs

Descriptive exceptions are used to make errors easier to identify during execution.

18. Project Structure
RetailVision/
│
├── data/
│   ├── input/
│   ├── sample/
│   └── yolo/
│
├── docs/
│   ├── architecture.md
│   ├── use_case.md
│   ├── class_diagram.md
│   ├── sequence_diagram.md
│   ├── component_diagram.md
│   └── testing.md
│
├── models/
│   └── retailvision_v2.pt
│
├── outputs/
│   └── detections/
│
├── src/
│   ├── analysis/
│   │   └── shelf_analyzer.py
│   ├── analytics/
│   │   └── inventory_analyzer.py
│   ├── data/
│   │   └── prepare_dataset.py
│   ├── detection/
│   │   └── product_detector.py
│   ├── preprocessing/
│   │   └── image_preprocessor.py
│   ├── visualization/
│   │   └── result_visualizer.py
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
19. Documentation

Detailed project documentation is available in the docs/ directory.

Architecture

docs/architecture.md

Contains the system architecture, data flow, technology stack, model information, and design rationale.

Use Case Diagram

docs/use_case.md

Describes the system actors and major user interactions.

Class Diagram

docs/class_diagram.md

Documents the major classes and their relationships.

Sequence Diagram

docs/sequence_diagram.md

Shows the interaction sequence between the user and major system components.

Component Diagram

docs/component_diagram.md

Shows the modular architecture and relationships between system components.

Testing Documentation

docs/testing.md

Contains testing scope, validation results, model metrics, and testing conclusions.

20. Design Decisions
Modular Architecture

Different responsibilities are separated into independent modules to improve maintainability and testing.

YOLO-Based Detection

YOLO was selected because the project requires object detection with bounding boxes and confidence scores.

Zone-Based Occupancy

The shelf image is divided into five horizontal zones. Detection overlap within each zone is used to estimate occupancy.

Automated Testing

Pytest is used to validate core modules and reduce the possibility of regression during development.

Git Version Control

Git is used to maintain project history and GitHub is used as the project repository.

21. Non-Functional Requirements
Performance

The system should process an input image through the detection and analytics pipeline without unnecessary processing overhead.

Usability

The command-line interface accepts the image path, model path, and confidence threshold as configurable inputs.

Reliability

Input validation and exception handling are implemented across major modules.

Maintainability

The system is divided into independent modules with documented responsibilities.

Scalability

The architecture allows future integration of additional models, databases, dashboards, or real-time camera input.

Resource Efficiency

Large datasets, model weights, generated outputs, and virtual-environment files are excluded from Git tracking where appropriate.

22. Challenges

During development, several practical challenges were addressed:

Converting the original dataset annotations into YOLO format
Preparing the training and validation split
Training the custom detection model on CPU
Managing large dataset and model files
Integrating detection results with analytics modules
Implementing automated tests
Organizing project documentation and UML diagrams
23. Future Enhancements

Possible future improvements include:

Real-time camera-based shelf monitoring
More detailed product-category classification
Database integration for historical inventory tracking
Web dashboard for store managers
Automated restocking recommendations
Multi-shelf and multi-store analytics
Improved detection accuracy through larger training datasets
Historical trend analysis
24. Repository

GitHub Repository:

RetailVision

https://github.com/PrabhavSharma16/RetailVision
25. Project Status
Project Development : Completed
Automated Tests      : 23/23 Passed
Model Training       : Completed
Model Validation     : Completed
Pipeline Integration : Completed
UML Documentation    : Completed
Testing Documentation: Completed
GitHub Repository    : Maintained
26. Conclusion

RetailVision provides a modular computer vision pipeline for intelligent retail shelf monitoring.

The system combines YOLO-based object detection with shelf occupancy analysis, inventory analytics, and result visualization. The final implementation has been validated through automated software tests and model evaluation.

The architecture is designed to support future extensions such as real-time monitoring, dashboards, database integration, and larger-scale retail analytics.