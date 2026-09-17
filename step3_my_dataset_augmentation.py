import cv2
import numpy as np
import os


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FOLDER = os.path.join(BASE_DIR, "my_dataset")
POSTER_PATH = os.path.join(BASE_DIR, "dataset", "Castle.jfif")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "results")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# --------------------------------------------------
# ArUco detector
# --------------------------------------------------

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_5X5_50
)

parameters = cv2.aruco.DetectorParameters()

detector = cv2.aruco.ArucoDetector(
    ARUCO_DICT,
    parameters
)


# --------------------------------------------------
# Load poster
# --------------------------------------------------

poster = cv2.imread(POSTER_PATH)

if poster is None:
    raise FileNotFoundError(
        f"Could not load poster: {POSTER_PATH}"
    )

poster_height, poster_width = poster.shape[:2]

print("Poster loaded:")
print("Width :", poster_width)
print("Height:", poster_height)


# --------------------------------------------------
# Process each scene
# --------------------------------------------------

image_files = [
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

image_files.sort()

print("\nNumber of images:", len(image_files))


for filename in image_files:

    print("\n--------------------------------------")
    print("Image:", filename)

    image_path = os.path.join(INPUT_FOLDER, filename)
    image = cv2.imread(image_path)

    if image is None:
        print("Could not read image.")
        continue


    # --------------------------------------------------
    # Detect ArUco marker
    # --------------------------------------------------

    corners, ids, rejected = detector.detectMarkers(image)

    if ids is None:
        print("Marker not detected.")
        continue

    # Find marker ID 7
    marker_index = None

    for i, marker_id in enumerate(ids.flatten()):
        if marker_id == 7:
            marker_index = i
            break

    if marker_index is None:
        print("Marker ID 7 not found.")
        continue


    # --------------------------------------------------
    # Get marker corners
    # --------------------------------------------------

    marker_corners = corners[marker_index][0].astype(np.float32)

    top_left = marker_corners[0]
    top_right = marker_corners[1]
    bottom_right = marker_corners[2]
    bottom_left = marker_corners[3]


    print("Marker ID: 7")
    print("Corners:")
    print(marker_corners)


    # --------------------------------------------------
    # Calculate marker centre
    # --------------------------------------------------

    center = (
        top_left +
        top_right +
        bottom_right +
        bottom_left
    ) / 4.0


    # --------------------------------------------------
    # Estimate marker width and height
    # --------------------------------------------------

    width_top = np.linalg.norm(top_right - top_left)
    width_bottom = np.linalg.norm(bottom_right - bottom_left)

    height_left = np.linalg.norm(bottom_left - top_left)
    height_right = np.linalg.norm(bottom_right - top_right)

    marker_width = (width_top + width_bottom) / 2
    marker_height = (height_left + height_right) / 2


    # --------------------------------------------------
    # Calculate directions of the marker plane
    # --------------------------------------------------

    horizontal_direction = (
        (top_right - top_left) +
        (bottom_right - bottom_left)
    ) / 2

    horizontal_direction = (
        horizontal_direction /
        np.linalg.norm(horizontal_direction)
    )

    vertical_direction = (
        (bottom_left - top_left) +
        (bottom_right - top_right)
    ) / 2

    vertical_direction = (
        vertical_direction /
        np.linalg.norm(vertical_direction)
    )


    # --------------------------------------------------
    # Define the target poster size
    # --------------------------------------------------

    # Make the poster larger than the ArUco marker.
    target_width = marker_width * 3.5

    poster_aspect_ratio = poster_width / poster_height

    target_height = target_width / poster_aspect_ratio


    # --------------------------------------------------
    # Calculate four target corners
    # --------------------------------------------------

    half_width = target_width / 2
    half_height = target_height / 2

    target_top_left = (
        center
        - horizontal_direction * half_width
        - vertical_direction * half_height
    )

    target_top_right = (
        center
        + horizontal_direction * half_width
        - vertical_direction * half_height
    )

    target_bottom_right = (
        center
        + horizontal_direction * half_width
        + vertical_direction * half_height
    )

    target_bottom_left = (
        center
        - horizontal_direction * half_width
        + vertical_direction * half_height
    )


    target_points = np.array([
        target_top_left,
        target_top_right,
        target_bottom_right,
        target_bottom_left
    ], dtype=np.float32)


    print("\nTarget poster corners:")
    print(target_points)


    # --------------------------------------------------
    # Source poster corners
    # --------------------------------------------------

    source_points = np.array([
        [0, 0],
        [poster_width - 1, 0],
        [poster_width - 1, poster_height - 1],
        [0, poster_height - 1]
    ], dtype=np.float32)


    # --------------------------------------------------
    # Calculate homography
    # --------------------------------------------------

    H, status = cv2.findHomography(
        source_points,
        target_points
    )

    if H is None:
        print("Homography calculation failed.")
        continue

    print("\nHomography matrix:")
    print(H)


    # --------------------------------------------------
    # Warp poster
    # --------------------------------------------------

    image_height, image_width = image.shape[:2]

    warped_poster = cv2.warpPerspective(
        poster,
        H,
        (image_width, image_height)
    )


    # --------------------------------------------------
    # Create mask
    # --------------------------------------------------

    poster_mask = np.zeros(
        (image_height, image_width),
        dtype=np.uint8
    )

    cv2.fillConvexPoly(
        poster_mask,
        target_points.astype(np.int32),
        255
    )


    # --------------------------------------------------
    # Combine poster with original image
    # --------------------------------------------------

    result = image.copy()

    result[poster_mask == 255] = (
        warped_poster[poster_mask == 255]
    )


    # --------------------------------------------------
    # Save result
    # --------------------------------------------------

    output_filename = "augmented_" + filename
    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    cv2.imwrite(output_path, result)

    print("\nSaved:")
    print(output_path)


print("\n======================================")
print("Augmentation finished.")
print("======================================")