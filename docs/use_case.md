# RetailVision Use Case Diagram

## System Actors

- **User** — Provides the retail shelf image and views the analysis results.
- **RetailVision System** — Processes the image and generates computer vision and inventory analytics.

## Use Cases

1. Upload / Select Shelf Image
2. Validate Input Image
3. Detect Products
4. Analyze Shelf Occupancy
5. Analyze Inventory
6. Identify Low-Stock Conditions
7. Generate Visualization
8. View Analysis Results
9. Save Annotated Output

## Use Case Flow

```mermaid
flowchart LR

    U[User]

    subgraph RV[RetailVision System]

        UC1[Select Shelf Image]
        UC2[Validate Input]
        UC3[Detect Products]
        UC4[Analyze Shelf Occupancy]
        UC5[Analyze Inventory]
        UC6[Identify Low-Stock Conditions]
        UC7[Generate Visualization]
        UC8[View Analysis Results]
        UC9[Save Annotated Output]

    end

    U --> UC1
    UC1 --> UC2
    UC2 --> UC3
    UC3 --> UC4
    UC3 --> UC5
    UC4 --> UC6
    UC5 --> UC6
    UC6 --> UC7
    UC7 --> UC8
    UC7 --> UC9
    UC8 --> U
Use Case Descriptions
Use Case	Description
Select Shelf Image	User provides a retail shelf image for analysis.
Validate Input	System checks whether the image exists and can be read.
Detect Products	YOLO model detects objects and generates bounding boxes and confidence scores.
Analyze Shelf Occupancy	System estimates occupancy across shelf analysis zones.
Analyze Inventory	System calculates inventory-related statistics from detections.
Identify Low-Stock Conditions	System identifies potentially low-stock products or shelf zones using configured thresholds.
Generate Visualization	System draws detection results and analytics on the input image.
View Analysis Results	User views the generated analytics and detection results.
Save Annotated Output	System saves the final annotated image for later use.