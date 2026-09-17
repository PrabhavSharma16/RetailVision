# RetailVision Component Diagram

## System Components

```mermaid
flowchart LR

    User["User"]

    UI["Input / CLI Interface"]

    Main["Main Pipeline<br/>src/main.py"]

    Pre["Image Preprocessing<br/>src/preprocessing"]

    Detect["Product Detection<br/>YOLO Model"]

    Shelf["Shelf Analysis<br/>src/analysis"]

    Inventory["Inventory Analytics<br/>src/analytics"]

    Visual["Result Visualization<br/>src/visualization"]

    Model["Trained Model<br/>retailvision_v2.pt"]

    Output["Annotated Output<br/>outputs/detections"]

    Config["Configuration<br/>src/config.py"]

    User --> UI
    UI --> Main

    Main --> Config
    Main --> Pre
    Pre --> Detect

    Model --> Detect

    Detect --> Shelf
    Detect --> Inventory

    Shelf --> Visual
    Inventory --> Visual

    Main --> Visual
    Visual --> Output
    Output --> User
Component Responsibilities
1. Input / CLI Interface

Provides the entry point through which the user supplies:

Shelf image path
Model path
Detection confidence threshold
2. Main Pipeline

The main orchestration component responsible for coordinating the complete RetailVision workflow.

It connects preprocessing, detection, shelf analysis, inventory analysis, and visualization components.

3. Image Preprocessing

Provides image preparation utilities such as:

Image loading
Image validation
Image resizing
Pixel normalization
4. Product Detection

Uses the trained YOLO model to identify objects in shelf images.

The component produces detection information including:

Class ID
Class name
Confidence
Bounding-box coordinates
5. Shelf Analysis

Processes detection results to calculate:

Total detected products
Product counts
Average detection confidence
Zone-wise shelf occupancy
Low-stock zones
6. Inventory Analytics

Converts detection information into inventory-level insights.

It calculates:

Total inventory
Unique product classes
Product frequency
Low-stock products
Dominant products
Inventory status
7. Result Visualization

Combines the detection and analytics results with the original image.

It generates:

Bounding boxes
Product labels
Confidence values
Shelf analytics
Inventory status
Low-stock zone information
8. Trained Model

The trained YOLO model is used by the Product Detection component for object detection.

The local trained model is:

models/retailvision_v2.pt

Model weights are excluded from Git tracking because of their size.

9. Annotated Output

The final processed image is saved in:

outputs/detections/

The output provides a visual representation of detected products together with the generated shelf and inventory analytics.

10. Configuration

The configuration component stores reusable system parameters such as:

Directory paths
Model name
Confidence threshold
IoU threshold
Supported image extensions
Component Interaction
Input Image
     ↓
Input / CLI Interface
     ↓
Main Pipeline
     ↓
Image Preprocessing
     ↓
Product Detection ← Trained YOLO Model
     ↓
Detection Results
     ├───────────────┐
     ↓               ↓
Shelf Analysis   Inventory Analytics
     └───────┬───────┘
             ↓
      Result Visualization
             ↓
      Annotated Output
Architectural Principle

RetailVision follows a modular component-based architecture. Each major responsibility is isolated into a dedicated component, allowing individual modules to be tested, maintained, and extended independently.

This structure also allows future components such as a database, web dashboard, real-time camera input, or additional product-classification models to be integrated without redesigning the complete system.