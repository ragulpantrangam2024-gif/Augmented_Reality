# Simple Augmented Reality using ArUco Markers

A computer vision project that implements a simple marker-based Augmented Reality (AR) system using Python, OpenCV, ArUco markers, homography, and perspective transformation.

The system detects an ArUco marker in an image and projects a poster onto the marker while maintaining the correct perspective.

---

## Project Overview

The project is divided into two parts:

### Task 1.1 – Provided Dataset
- Detect ArUco markers in the provided image sequence.
- Extract the four marker corner points.
- Calculate a homography.
- Apply perspective transformation to a poster.
- Generate augmented images for the complete dataset.
- Evaluate the geometric accuracy of the augmentation.

### Task 1.2 – Own Recordings
- Use self-recorded images containing an ArUco marker.
- Detect the marker from different viewpoints.
- Project the same poster onto the marker.
- Demonstrate augmentation under perspective changes.

---

## Technologies

- Python
- OpenCV
- NumPy
- ArUco Marker Detection
- Homography
- Perspective Transformation

---

## How It Works

The complete AR pipeline is:

```text
Input Image
     ↓
ArUco Marker Detection
     ↓
Four Marker Corner Points
     ↓
Define Poster Corner Points
     ↓
Calculate Homography
     ↓
Perspective Transformation
     ↓
Warp Poster
     ↓
Overlay Poster on Image
     ↓
Augmented Image
     ↓
Geometric Evaluation
```

The four corners of the ArUco marker provide the reference points required to calculate the transformation.

---

# Project Structure

```text
Augmented_Reality/
│
├── README.md
├── .gitignore
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
│   ├── ...
│   └── Castle.jfif
│
├── my_dataset/
│   ├── scene_1.jpg
│   └── scene_2.jpg
│
└── results/
    ├── detected_*.jpg
    ├── my_detection_scene_1.jpg
    ├── my_detection_scene_2.jpg
    ├── step2_AR_*.jpg
    ├── step2_warped_*.jpg
    │
    ├── evaluation/
    │   ├── evaluation_*.jpg
    │   ├── evaluation_summary.csv
    │   └── evaluation_summary.txt
    │
    └── final_poster/
        ├── AR_*.jpg
        ├── augmented_scene_1.jpg
        └── augmented_scene_2.jpg
```

---

# Task 1.1 – Provided Dataset

## 1. ArUco Detection

The first step is detecting the ArUco marker in the provided dataset.

The program extracts:

- Marker ID
- Four marker corner coordinates
- Detected marker candidates
- Rejected candidates

### Script

```text
step1_aruco_detection.py
```

### Input

```text
dataset/
```

### Output

```text
results/detected_*.jpg
```

The dataset contains 11 images.

The marker was successfully detected in 10 images. One image did not produce a valid marker detection and was handled separately during evaluation.

---

## 2. Perspective Transformation

After detecting the marker, the four marker corners are used as reference points for placing the poster.

OpenCV is used to calculate and apply the transformation:

```python
cv2.getPerspectiveTransform()
cv2.warpPerspective()
```

### Script

```text
step2_perspective_transform.py
```

---

## 3. Homography

A homography is a 3 × 3 projective transformation matrix that maps points between two planar surfaces.

In this project:

```text
Poster coordinates
       ↓
   Homography
       ↓
Marker / Image coordinates
```

The homography allows the poster to follow the orientation and perspective of the marker.

---

## 4. Poster Augmentation

The poster used in this project is:

```text
dataset/Castle.jfif
```

The same poster is used for all images so that the results remain comparable.

The poster is:

1. Loaded.
2. Mapped to the marker coordinates.
3. Perspective warped.
4. Combined with the original image.

### Script

```text
step3_process_all_images.py
```

### Final results

```text
results/final_poster/
```

---

# Task 1.2 – Own Recordings

For the second part, two images were recorded using a printed ArUco marker.

```text
my_dataset/
├── scene_1.jpg
└── scene_2.jpg
```

The two scenes show the marker from different viewpoints.

## Marker Detection

The own recordings use:

```text
Dictionary: DICT_5X5_50
Marker ID: 7
```

### Script

```text
step2_my_dataset_detection.py
```

### Output

```text
results/my_detection_scene_1.jpg
results/my_detection_scene_2.jpg
```

## Own Image Augmentation

The same poster is projected onto the marker in both scenes.

### Script

```text
step3_my_dataset_augmentation.py
```

### Final results

```text
results/final_poster/augmented_scene_1.jpg
results/final_poster/augmented_scene_2.jpg
```

These results demonstrate that the poster follows the perspective of the marker in different viewpoints.

---

# Evaluation

The augmented images from the provided dataset are evaluated using:

```text
step4_evaluation.py
```

The evaluation checks the geometric alignment and perspective consistency of the projected poster.

The results are stored in:

```text
results/evaluation/
```

Including:

```text
evaluation_summary.csv
evaluation_summary.txt
```

The average angular error obtained from the evaluation is approximately:

```text
1.87°
```

A lower angular error indicates better alignment between the augmented poster edges and the reference geometry.

---

# How to Run

Install the required libraries:

```bash
pip install opencv-contrib-python numpy
```

Run the scripts from the project directory.

### Step 1 – Detect ArUco markers

```bash
python step1_aruco_detection.py
```

### Step 2 – Detect markers in own images

```bash
python step2_my_dataset_detection.py
```

### Step 3 – Test perspective transformation

```bash
python step2_perspective_transform.py
```

### Step 4 – Process the complete dataset

```bash
python step3_process_all_images.py
```

### Step 5 – Augment own images

```bash
python step3_my_dataset_augmentation.py
```

### Step 6 – Evaluate the results

```bash
python step4_evaluation.py
```

---

# Key Computer Vision Concepts

## ArUco Marker

A square fiducial marker that can be detected using computer vision. Its four corners provide reference points for geometric transformations.

## Homography

A projective transformation represented by a 3 × 3 matrix. It maps the poster from its original rectangular coordinates to the perspective of the marker.

## Perspective Transformation

Changes the shape of the poster so that it appears correctly aligned with the orientation and viewpoint of the marker.

## Augmented Reality

The transformed poster is overlaid onto the original image, creating the final augmented scene.

---

# Results

The project demonstrates:

- ArUco marker detection
- Marker corner extraction
- Homography calculation
- Perspective transformation
- Poster warping
- Image augmentation
- Processing of multiple images
- Geometric evaluation
- Augmentation on self-recorded images
- Different camera viewpoints

---

# Conclusion

This project implements a complete basic marker-based Augmented Reality pipeline using OpenCV.

The ArUco marker provides the geometric reference. Its four detected corners are used to calculate a homography, which transforms the poster according to the perspective of the scene.

The approach was tested on both the provided dataset and two self-recorded scenes with noticeable perspective changes.# Simple Augmented Reality using ArUco Markers

A computer vision project that implements a simple marker-based Augmented Reality (AR) system using Python, OpenCV, ArUco markers, homography, and perspective transformation.

The system detects an ArUco marker in an image and projects a poster onto the marker while maintaining the correct perspective.

---

## Project Overview

The project is divided into two parts:

### Task 1.1 – Provided Dataset
- Detect ArUco markers in the provided image sequence.
- Extract the four marker corner points.
- Calculate a homography.
- Apply perspective transformation to a poster.
- Generate augmented images for the complete dataset.
- Evaluate the geometric accuracy of the augmentation.

### Task 1.2 – Own Recordings
- Use self-recorded images containing an ArUco marker.
- Detect the marker from different viewpoints.
- Project the same poster onto the marker.
- Demonstrate augmentation under perspective changes.

---

## Technologies

- Python
- OpenCV
- NumPy
- ArUco Marker Detection
- Homography
- Perspective Transformation

---

## How It Works

The complete AR pipeline is:

```text
Input Image
     ↓
ArUco Marker Detection
     ↓
Four Marker Corner Points
     ↓
Define Poster Corner Points
     ↓
Calculate Homography
     ↓
Perspective Transformation
     ↓
Warp Poster
     ↓
Overlay Poster on Image
     ↓
Augmented Image
     ↓
Geometric Evaluation
```

The four corners of the ArUco marker provide the reference points required to calculate the transformation.

---

# Project Structure

```text
Augmented_Reality/
│
├── README.md
├── .gitignore
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
│   ├── ...
│   └── Castle.jfif
│
├── my_dataset/
│   ├── scene_1.jpg
│   └── scene_2.jpg
│
└── results/
    ├── detected_*.jpg
    ├── my_detection_scene_1.jpg
    ├── my_detection_scene_2.jpg
    ├── step2_AR_*.jpg
    ├── step2_warped_*.jpg
    │
    ├── evaluation/
    │   ├── evaluation_*.jpg
    │   ├── evaluation_summary.csv
    │   └── evaluation_summary.txt
    │
    └── final_poster/
        ├── AR_*.jpg
        ├── augmented_scene_1.jpg
        └── augmented_scene_2.jpg
```

---

# Task 1.1 – Provided Dataset

## 1. ArUco Detection

The first step is detecting the ArUco marker in the provided dataset.

The program extracts:

- Marker ID
- Four marker corner coordinates
- Detected marker candidates
- Rejected candidates

### Script

```text
step1_aruco_detection.py
```

### Input

```text
dataset/
```

### Output

```text
results/detected_*.jpg
```

The dataset contains 11 images.

The marker was successfully detected in 10 images. One image did not produce a valid marker detection and was handled separately during evaluation.

---

## 2. Perspective Transformation

After detecting the marker, the four marker corners are used as reference points for placing the poster.

OpenCV is used to calculate and apply the transformation:

```python
cv2.getPerspectiveTransform()
cv2.warpPerspective()
```

### Script

```text
step2_perspective_transform.py
```

---

## 3. Homography

A homography is a 3 × 3 projective transformation matrix that maps points between two planar surfaces.

In this project:

```text
Poster coordinates
       ↓
   Homography
       ↓
Marker / Image coordinates
```

The homography allows the poster to follow the orientation and perspective of the marker.

---

## 4. Poster Augmentation

The poster used in this project is:

```text
dataset/Castle.jfif
```

The same poster is used for all images so that the results remain comparable.

The poster is:

1. Loaded.
2. Mapped to the marker coordinates.
3. Perspective warped.
4. Combined with the original image.

### Script

```text
step3_process_all_images.py
```

### Final results

```text
results/final_poster/
```

---

# Task 1.2 – Own Recordings

For the second part, two images were recorded using a printed ArUco marker.

```text
my_dataset/
├── scene_1.jpg
└── scene_2.jpg
```

The two scenes show the marker from different viewpoints.

## Marker Detection

The own recordings use:

```text
Dictionary: DICT_5X5_50
Marker ID: 7
```

### Script

```text
step2_my_dataset_detection.py
```

### Output

```text
results/my_detection_scene_1.jpg
results/my_detection_scene_2.jpg
```

## Own Image Augmentation

The same poster is projected onto the marker in both scenes.

### Script

```text
step3_my_dataset_augmentation.py
```

### Final results

```text
results/final_poster/augmented_scene_1.jpg
results/final_poster/augmented_scene_2.jpg
```

These results demonstrate that the poster follows the perspective of the marker in different viewpoints.

---

# Evaluation

The augmented images from the provided dataset are evaluated using:

```text
step4_evaluation.py
```

The evaluation checks the geometric alignment and perspective consistency of the projected poster.

The results are stored in:

```text
results/evaluation/
```

Including:

```text
evaluation_summary.csv
evaluation_summary.txt
```

The average angular error obtained from the evaluation is approximately:

```text
1.87°
```

A lower angular error indicates better alignment between the augmented poster edges and the reference geometry.

---

# How to Run

Install the required libraries:

```bash
pip install opencv-contrib-python numpy
```

Run the scripts from the project directory.

### Step 1 – Detect ArUco markers

```bash
python step1_aruco_detection.py
```

### Step 2 – Detect markers in own images

```bash
python step2_my_dataset_detection.py
```

### Step 3 – Test perspective transformation

```bash
python step2_perspective_transform.py
```

### Step 4 – Process the complete dataset

```bash
python step3_process_all_images.py
```

### Step 5 – Augment own images

```bash
python step3_my_dataset_augmentation.py
```

### Step 6 – Evaluate the results

```bash
python step4_evaluation.py
```

---

# Key Computer Vision Concepts

## ArUco Marker

A square fiducial marker that can be detected using computer vision. Its four corners provide reference points for geometric transformations.

## Homography

A projective transformation represented by a 3 × 3 matrix. It maps the poster from its original rectangular coordinates to the perspective of the marker.

## Perspective Transformation

Changes the shape of the poster so that it appears correctly aligned with the orientation and viewpoint of the marker.

## Augmented Reality

The transformed poster is overlaid onto the original image, creating the final augmented scene.

---

# Results

The project demonstrates:

- ArUco marker detection
- Marker corner extraction
- Homography calculation
- Perspective transformation
- Poster warping
- Image augmentation
- Processing of multiple images
- Geometric evaluation
- Augmentation on self-recorded images
- Different camera viewpoints

---

# Conclusion

This project implements a complete basic marker-based Augmented Reality pipeline using OpenCV.

The ArUco marker provides the geometric reference. Its four detected corners are used to calculate a homography, which transforms the poster according to the perspective of the scene.

The approach was tested on both the provided dataset and two self-recorded scenes with noticeable perspective changes.