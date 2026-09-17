# Simple Augmented Reality using ArUco Markers

## Overview

This project implements a simple Augmented Reality (AR) system using **ArUco marker detection, homography estimation, and perspective transformation** with OpenCV.

The objective is to detect an ArUco marker in images and use its four corner points to determine where a poster should be projected onto the scene. The same poster is then augmented onto the marker location while preserving the perspective of the scene.

The project consists of two parts:

- **Task 1.1:** Augmentation using the provided "Room with ArUco Markers" dataset.
- **Task 1.2:** Augmentation using two self-recorded images with an ArUco marker.

---

## Project Structure

```text
Augmented_Reality/
│
├── .gitignore
├── README.md
│
├── step1_aruco_detection.py
├── step2_my_dataset_detection.py
├── step2_perspective_transform.py
├── step3_my_dataset_augmentation.py
├── step3_process_all_images.py
├── step4_evaluation.py
│
├── dataset/
│   ├── 20221115_113319.jpg
│   ├── 20221115_113328.jpg
│   ├── 20221115_113340.jpg
│   ├── 20221115_113346.jpg
│   ├── 20221115_113356.jpg
│   ├── 20221115_113401.jpg
│   ├── 20221115_113412.jpg
│   ├── 20221115_113424.jpg
│   ├── 20221115_113437.jpg
│   ├── 20221115_113440.jpg
│   ├── 20221115_113635.jpg
│   └── Castle.jfif
│
├── my_dataset/
│   ├── scene_1.jpg
│   └── scene_2.jpg
│
└── results/
    │
    ├── detected_20221115_113319.jpg
    ├── detected_20221115_113328.jpg
    ├── detected_20221115_113340.jpg
    ├── detected_20221115_113346.jpg
    ├── detected_20221115_113356.jpg
    ├── detected_20221115_113401.jpg
    ├── detected_20221115_113412.jpg
    ├── detected_20221115_113424.jpg
    ├── detected_20221115_113437.jpg
    ├── detected_20221115_113440.jpg
    ├── detected_20221115_113635.jpg
    │
    ├── my_detection_scene_1.jpg
    ├── my_detection_scene_2.jpg
    │
    ├── step2_AR_20221115_113319.jpg
    ├── step2_warped_20221115_113319.jpg
    │
    ├── evaluation/
    │   ├── evaluation_AR_20221115_113319.jpg
    │   ├── evaluation_AR_20221115_113328.jpg
    │   ├── evaluation_AR_20221115_113340.jpg
    │   ├── evaluation_AR_20221115_113346.jpg
    │   ├── evaluation_AR_20221115_113356.jpg
    │   ├── evaluation_AR_20221115_113401.jpg
    │   ├── evaluation_AR_20221115_113412.jpg
    │   ├── evaluation_AR_20221115_113424.jpg
    │   ├── evaluation_AR_20221115_113437.jpg
    │   ├── evaluation_AR_20221115_113440.jpg
    │   ├── evaluation_FAILED_20221115_113635.jpg
    │   ├── evaluation_summary.csv
    │   └── evaluation_summary.txt
    │
    └── final_poster/
        ├── AR_20221115_113319.jpg
        ├── AR_20221115_113328.jpg
        ├── AR_20221115_113340.jpg
        ├── AR_20221115_113346.jpg
        ├── AR_20221115_113356.jpg
        ├── AR_20221115_113401.jpg
        ├── AR_20221115_113412.jpg
        ├── AR_20221115_113424.jpg
        ├── AR_20221115_113437.jpg
        ├── AR_20221115_113440.jpg
        ├── augmented_scene_1.jpg
        └── augmented_scene_2.jpg
1. Technologies Used
Python
OpenCV
NumPy
ArUco marker detection
Homography
Perspective transformation
2. Task 1.1 — Provided Dataset
2.1 ArUco Marker Detection

The first step is to detect ArUco markers in every image of the provided dataset.

The implementation uses OpenCV's ArUco detector and identifies:

Marker ID
Four marker corner coordinates
Detected and rejected marker candidates

The marker detection is implemented in:

step1_aruco_detection.py
Input

The input images are stored in:

dataset/

The folder contains 11 images.

Output

The detected marker results are stored in:

results/

with filenames beginning with:

detected_

The detected marker corners are used as the geometric reference for the following perspective transformation.

3. ArUco Marker Detection Result

The provided dataset contains 11 images.

The detector successfully identified the ArUco marker in 10 images.

One image:

20221115_113635.jpg

did not produce a valid marker detection and was therefore treated separately during the evaluation.

The detected marker in the successful frames has:

Marker ID: 0

The four detected corner points define the quadrilateral corresponding to the marker in the image.

4. Task 1.1 — Perspective Transformation

After detecting the ArUco marker, the next step is to determine where the poster should be placed.

A perspective transformation is required because the marker can appear at different orientations and viewing angles.

The four detected ArUco corners provide four corresponding image points.

A rectangular poster is defined using four target points.

The relationship between the poster coordinates and the image coordinates is represented by a homography matrix.

The homography is calculated using OpenCV:

cv2.getPerspectiveTransform()

and the image is transformed using:

cv2.warpPerspective()

The implementation is contained in:

step2_perspective_transform.py
5. Homography

A homography is a 3 × 3 projective transformation matrix:

      | h11 h12 h13 |
H  =  | h21 h22 h23 |
      | h31 h32 h33 |

It maps points from one planar coordinate system to another.

For a point:

p = (x, y)

the transformed point is obtained using:

p' = H p

followed by normalization using the homogeneous coordinate.

In this project, the homography maps the rectangular poster onto the quadrilateral defined by the detected ArUco marker.

This allows the poster to follow the perspective of the scene.

6. Poster

The poster used for augmentation is:

dataset/Castle.jfif

The poster is loaded and its four corners are used as the source points for the perspective transformation.

The same poster is used throughout the dataset so that the augmented images remain comparable.

7. AR Augmentation

Once the perspective transformation has been calculated, the poster is warped into the required position.

The transformed poster is then combined with the original image.

The complete augmentation process is implemented using:

step3_process_all_images.py

The final augmented images are stored in:

results/final_poster/

The generated files use the naming convention:

AR_<original_filename>.jpg

For example:

AR_20221115_113319.jpg
AR_20221115_113328.jpg
8. Intermediate Perspective Transformation Results

Intermediate results from the perspective transformation are also stored in:

results/

These include:

step2_AR_20221115_113319.jpg
step2_warped_20221115_113319.jpg

These images are useful for understanding the individual stages of the transformation before processing the complete dataset.

9. Task 1.2 — Own Recordings

For the second part of the task, two images were recorded using a printed ArUco marker.

The images are stored in:

my_dataset/
scene_1.jpg
scene_2.jpg

The two scenes show the marker from different viewpoints and therefore demonstrate perspective changes.

10. Own Dataset Marker Detection

The ArUco marker in the self-recorded images uses:

Dictionary: DICT_5X5_50
Marker ID: 7

The detection is implemented in:

step2_my_dataset_detection.py

The resulting marker detection images are:

results/my_detection_scene_1.jpg
results/my_detection_scene_2.jpg

The detector provides four corner coordinates for each marker.

These points are subsequently used for the perspective transformation.

11. Own Dataset Augmentation

The poster is also projected onto the marker in the two self-recorded scenes.

The augmentation is implemented in:

step3_my_dataset_augmentation.py

The final results are:

results/final_poster/augmented_scene_1.jpg
results/final_poster/augmented_scene_2.jpg

These images demonstrate that the poster follows the perspective of the marker in both scenes.

12. Evaluation

The augmented images from the provided dataset are evaluated using:

step4_evaluation.py

The evaluation results are stored separately in:

results/evaluation/

The evaluation directory contains:

Augmented images used for evaluation
A failed-detection evaluation image
A CSV summary
A text summary

The summary files are:

evaluation_summary.csv
evaluation_summary.txt

The evaluation also includes:

evaluation_FAILED_20221115_113635.jpg

for the image where the ArUco marker could not be detected.

The evaluation is based on the visual/geometrical correctness of the augmentation, particularly whether the poster is correctly positioned and follows the perspective of the marker.

13. Complete Processing Pipeline

The complete workflow can be summarized as follows:

Input Image
     │
     ▼
ArUco Marker Detection
     │
     ▼
Marker ID + Four Corner Points
     │
     ▼
Define Poster Corner Points
     │
     ▼
Calculate Homography
     │
     ▼
Perspective Transformation
     │
     ▼
Warp Poster
     │
     ▼
Combine Poster with Original Image
     │
     ▼
Augmented Reality Image
     │
     ▼
Visual / Geometrical Evaluation
14. How to Run
Step 1 — Detect ArUco Markers

Run:

python step1_aruco_detection.py

This processes the images in:

dataset/

and stores the marker detection results in:

results/
Step 2 — Test ArUco Detection on Own Images

Run:

python step2_my_dataset_detection.py

This processes:

my_dataset/scene_1.jpg
my_dataset/scene_2.jpg

and generates:

results/my_detection_scene_1.jpg
results/my_detection_scene_2.jpg
Step 3 — Perspective Transformation

Run:

python step2_perspective_transform.py

This demonstrates the perspective transformation using the detected marker coordinates.

Step 4 — Process the Dataset

Run:

python step3_process_all_images.py

This processes the provided dataset and generates the final AR images.

The results are stored in:

results/final_poster/
Step 5 — Augment Own Images

Run:

python step3_my_dataset_augmentation.py

This generates:

results/final_poster/augmented_scene_1.jpg
results/final_poster/augmented_scene_2.jpg
Step 6 — Evaluation

Run:

python step4_evaluation.py

The evaluation results are stored in:

results/evaluation/
15. Results

The project successfully demonstrates the main stages of a simple marker-based Augmented Reality system:

Detection of ArUco markers.
Extraction of the four marker corner points.
Definition of corresponding poster points.
Computation of a homography.
Perspective warping of the poster.
Projection of the poster into the scene.
Processing of the provided image sequence.
Evaluation of the resulting augmentation.
Testing on two self-recorded scenes with perspective changes.

The final augmented images can be found in:

results/final_poster/
16. Key Concepts
ArUco Marker

An ArUco marker is a square fiducial marker containing a binary pattern that can be detected by computer vision algorithms.

In this project, the marker provides a stable set of four image points.

Homography

A homography describes the projective relationship between two planar surfaces.

It is used here to map the rectangular poster to the perspective of the detected marker.

Perspective Transformation

Perspective transformation changes the appearance of the poster so that it matches the orientation and perspective of the marker in the input image.

Augmented Reality

The transformed poster is overlaid onto the original image, creating the final augmented scene.

17. Conclusion

This project implements a complete basic marker-based Augmented Reality pipeline using OpenCV.

The ArUco marker acts as the geometric reference. Once its four corners are detected, a homography can be calculated between the poster and the marker. The poster is then transformed using a perspective transformation and placed into the scene.

The approach works across different viewpoints in the provided dataset and is additionally demonstrated using two self-recorded scenes with noticeable perspective changes.