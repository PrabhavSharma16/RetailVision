# RetailVision Testing & Validation

## 1. Testing Overview

RetailVision was tested at both the module level and integrated pipeline level to verify that the major components work correctly and produce valid outputs.

The project uses **Pytest** for automated software testing.

### Test Command

```bash
python -m pytest -q
Final Test Result
23 passed in 1.54s

All 23 automated tests passed successfully.

2. Testing Scope

The testing process covers the following major components:

Component	Testing Focus
Image Preprocessing	Image loading, resizing, normalization and invalid input handling
Shelf Analyzer	Product counting, confidence calculation and occupancy analysis
Inventory Analyzer	Inventory counting, product classification and stock status
Result Visualizer	Detection drawing, summary panel and output image generation
Integrated Pipeline	End-to-end execution using the trained YOLO model
3. Image Preprocessing Tests

The preprocessing module was tested for:

Successful image loading
Image resizing to the required dimensions
Pixel normalization
Handling of missing image files
Handling of invalid image input

These tests verify that the input-processing component behaves correctly before computer vision inference.

4. Shelf Analysis Tests

The Shelf Analyzer was tested for:

Correct product counting
Correct calculation of total detections
Average confidence calculation
Zone-based shelf occupancy calculation
Identification of low-stock zones
Handling of empty detection results
Validation of invalid image dimensions

The tests confirm that detection results can be converted into meaningful shelf-level measurements.

5. Inventory Analytics Tests

The Inventory Analyzer was tested for:

Product frequency calculation
Total inventory calculation
Unique product counting
Low-stock product identification
Dominant product identification
Inventory status generation
Empty inventory handling
Inventory summary generation

These tests validate the conversion of computer vision detections into inventory insights.

6. Visualization Tests

The Result Visualizer was tested for:

Drawing detection bounding boxes
Generating the analytics summary panel
Saving annotated images
Handling invalid image input
Validating summary-panel input

The visualization tests ensure that analytical results can be correctly represented in the final output image.

7. Integrated Pipeline Validation

The complete RetailVision pipeline was executed using the trained model:

Input Shelf Image
        ↓
YOLO Product Detection
        ↓
Shelf Analysis
        ↓
Inventory Analysis
        ↓
Result Visualization
        ↓
Annotated Output Image

The integrated pipeline completed successfully and generated:

outputs/detections/retailvision_result.jpg

The tested execution produced detection results along with shelf occupancy and inventory analytics.

8. Model Validation

The trained RetailVision YOLO model was evaluated on the validation dataset.

Final validation metrics obtained at 640 image size were:

Metric	Result
Precision	0.543
Recall	0.442
mAP@50	0.385
mAP@50-95	0.165

Per-class mAP@50:

Class	mAP@50
Product	0.396
Price	0.373

These metrics provide an objective measurement of the trained detection model on the validation data.

9. Test Dataset

The prepared dataset contains:

45 total images
36 training images
9 validation images
2 object classes
Product
Price

The dataset annotations were converted from the original annotation format into YOLO-compatible bounding-box labels.

10. Test Result Summary
Automated Tests : 23
Passed          : 23
Failed          : 0

Test Duration   : 1.54 seconds

Therefore, all automated software tests passed successfully.

11. Error Handling Validation

The system includes validation for common input errors such as:

Missing image files
Unreadable images
Empty image inputs
Invalid image dimensions
Invalid visualization inputs
Missing model files

Exceptions are raised with descriptive messages so that incorrect inputs can be identified during execution.

12. Testing Conclusion

The testing process verifies the major functional modules of RetailVision and confirms that the integrated pipeline executes successfully.

The automated test suite achieved:

23/23 tests passed

The trained detection model was additionally evaluated using standard object-detection metrics including Precision, Recall, mAP@50, and mAP@50-95.