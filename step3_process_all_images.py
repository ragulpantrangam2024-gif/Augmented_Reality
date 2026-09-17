import cv2
import numpy as np
import os


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FOLDER = os.path.join(
    BASE_DIR,
    "dataset"
)

POSTER_PATH = os.path.join(
    INPUT_FOLDER,
    "Castle.jfif"
)

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "results"
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# ============================================================
# 2. PARAMETERS
# ============================================================

# Controls how large the poster is compared
# with the detected ArUco marker.
SCALE = 4.0


# ============================================================
# 3. LOAD POSTER
# ============================================================

poster = cv2.imread(POSTER_PATH)

if poster is None:
    raise FileNotFoundError(
        f"Could not load poster: {POSTER_PATH}"
    )

poster_height, poster_width = poster.shape[:2]

print("Poster loaded successfully")
print("Poster size:", poster_width, "x", poster_height)


# ============================================================
# 4. CREATE ARUCO DETECTOR
# ============================================================

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_6X6_50
)

parameters = cv2.aruco.DetectorParameters()

detector = cv2.aruco.ArucoDetector(
    ARUCO_DICT,
    parameters
)


# ============================================================
# 5. FUNCTION: AUGMENT ONE IMAGE
# ============================================================

def augment_image(image, image_name):

    # --------------------------------------------------------
    # Detect ArUco markers
    # --------------------------------------------------------

    corners, ids, rejected = detector.detectMarkers(
        image
    )

    # --------------------------------------------------------
    # No marker detected
    # --------------------------------------------------------

    if ids is None:

        print(
            f"{image_name}: "
            "NO MARKER DETECTED"
        )

        return None

    # --------------------------------------------------------
    # Find marker ID 0
    # --------------------------------------------------------

    marker_index = None

    for i, marker_id in enumerate(ids.flatten()):

        if marker_id == 0:
            marker_index = i
            break

    # If marker 0 is not present
    if marker_index is None:

        print(
            f"{image_name}: "
            "Marker ID 0 not found"
        )

        return None

    # --------------------------------------------------------
    # Get four corners of marker
    # --------------------------------------------------------

    marker_corners = corners[marker_index][0]

    # --------------------------------------------------------
    # Calculate marker center
    # --------------------------------------------------------

    marker_center = np.mean(
        marker_corners,
        axis=0
    )

    # --------------------------------------------------------
    # Expand marker quadrilateral
    # --------------------------------------------------------

    expanded_corners = (
        marker_center
        + SCALE * (
            marker_corners
            - marker_center
        )
    )

    expanded_corners = np.float32(
        expanded_corners
    )

    # --------------------------------------------------------
    # Define poster corners
    # --------------------------------------------------------

    source_points = np.float32([
        [0, 0],

        [poster_width - 1, 0],

        [
            poster_width - 1,
            poster_height - 1
        ],

        [
            0,
            poster_height - 1
        ]
    ])

    # --------------------------------------------------------
    # Calculate homography
    # --------------------------------------------------------

    H, status = cv2.findHomography(
        source_points,
        expanded_corners
    )

    if H is None:

        print(
            f"{image_name}: "
            "Homography calculation failed"
        )

        return None

    # --------------------------------------------------------
    # Warp poster
    # --------------------------------------------------------

    warped_poster = cv2.warpPerspective(
        poster,
        H,
        (
            image.shape[1],
            image.shape[0]
        )
    )

    # --------------------------------------------------------
    # Create poster mask
    # --------------------------------------------------------

    mask = np.zeros(
        image.shape[:2],
        dtype=np.uint8
    )

    cv2.fillConvexPoly(
        mask,
        np.int32(expanded_corners),
        255
    )

    # --------------------------------------------------------
    # Keep original image outside poster
    # --------------------------------------------------------

    inverse_mask = cv2.bitwise_not(
        mask
    )

    background = cv2.bitwise_and(
        image,
        image,
        mask=inverse_mask
    )

    # --------------------------------------------------------
    # Keep only warped poster area
    # --------------------------------------------------------

    poster_area = cv2.bitwise_and(
        warped_poster,
        warped_poster,
        mask=mask
    )

    # --------------------------------------------------------
    # Combine background and poster
    # --------------------------------------------------------

    augmented_image = cv2.add(
        background,
        poster_area
    )

    return augmented_image


# ============================================================
# 6. FIND ALL DATASET IMAGES
# ============================================================

image_files = []

for filename in os.listdir(INPUT_FOLDER):

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension in [
        ".jpg",
        ".jpeg",
        ".png"
    ]:

        image_files.append(filename)


image_files.sort()


print("\nNumber of images found:", len(image_files))

print("\nImages to process:")

for filename in image_files:

    print(" -", filename)


# ============================================================
# 7. PROCESS ALL IMAGES
# ============================================================

detected_count = 0
failed_count = 0

print("\n")
print("=" * 60)
print("STARTING AR AUGMENTATION")
print("=" * 60)


for filename in image_files:

    image_path = os.path.join(
        INPUT_FOLDER,
        filename
    )

    image = cv2.imread(
        image_path
    )

    if image is None:

        print(
            f"{filename}: "
            "Could not load image"
        )

        failed_count += 1

        continue

    # --------------------------------------------------------
    # Run augmentation
    # --------------------------------------------------------

    augmented_image = augment_image(
        image,
        filename
    )

    # --------------------------------------------------------
    # Save result
    # --------------------------------------------------------

    if augmented_image is not None:

        output_filename = (
            "AR_" + filename
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            output_filename
        )

        cv2.imwrite(
            output_path,
            augmented_image
        )

        print(
            f"{filename}: "
            "AR image created"
        )

        detected_count += 1

    else:

        # Save original image with a special name
        # so we know that augmentation failed.

        output_filename = (
            "FAILED_" + filename
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            output_filename
        )

        cv2.imwrite(
            output_path,
            image
        )

        failed_count += 1


# ============================================================
# 8. FINAL SUMMARY
# ============================================================

print("\n")
print("=" * 60)
print("AR AUGMENTATION SUMMARY")
print("=" * 60)

print(
    "Total images:",
    len(image_files)
)

print(
    "Successfully augmented:",
    detected_count
)

print(
    "Failed:",
    failed_count
)

print("=" * 60)