import cv2
import numpy as np
import os


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FOLDER = os.path.join(BASE_DIR, "dataset")

POSTER_PATH = os.path.join(
    INPUT_FOLDER,
    "Castle.jfif"
)

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "results"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================
# 2. LOAD THE POSTER
# ============================================================

poster = cv2.imread(POSTER_PATH)

if poster is None:
    raise FileNotFoundError(
        f"Could not load poster: {POSTER_PATH}"
    )

poster_height, poster_width = poster.shape[:2]

print("Poster loaded successfully")
print("Poster width :", poster_width)
print("Poster height:", poster_height)


# ============================================================
# 3. LOAD ONE DATASET IMAGE
# ============================================================

image_name = "20221115_113319.jpg"

image_path = os.path.join(
    INPUT_FOLDER,
    image_name
)

image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(
        f"Could not load image: {image_path}"
    )

print("\nImage loaded:", image_name)
print(
    "Image size:",
    image.shape[1],
    "x",
    image.shape[0]
)


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
# 5. DETECT ARUCO MARKER
# ============================================================

corners, ids, rejected = detector.detectMarkers(
    image
)

if ids is None:
    print("\nNo ArUco marker detected.")
    exit()

print("\nDetected marker IDs:")
print(ids.flatten())


# ============================================================
# 6. GET FOUR MARKER CORNERS
# ============================================================

marker_corners = corners[0][0]

print("\nDetected marker corners:")

print("Top-left     :", marker_corners[0])
print("Top-right    :", marker_corners[1])
print("Bottom-right :", marker_corners[2])
print("Bottom-left  :", marker_corners[3])


# ============================================================
# 7. CALCULATE MARKER CENTER
# ============================================================

marker_center = np.mean(
    marker_corners,
    axis=0
)

print("\nMarker center:")
print(marker_center)


# ============================================================
# 8. ENLARGE THE DESTINATION QUADRILATERAL
# ============================================================

# Enlargement factor
SCALE = 3.0

expanded_corners = (
    marker_center
    + SCALE * (marker_corners - marker_center)
)

expanded_corners = np.float32(
    expanded_corners
)

print("\nExpanded destination corners:")

print("Top-left     :", expanded_corners[0])
print("Top-right    :", expanded_corners[1])
print("Bottom-right :", expanded_corners[2])
print("Bottom-left  :", expanded_corners[3])


# ============================================================
# 9. DEFINE ORIGINAL POSTER CORNERS
# ============================================================

source_points = np.float32([
    [0, 0],
    [poster_width - 1, 0],
    [poster_width - 1, poster_height - 1],
    [0, poster_height - 1]
])


# ============================================================
# 10. CALCULATE HOMOGRAPHY
# ============================================================

H, status = cv2.findHomography(
    source_points,
    expanded_corners
)

print("\nHomography matrix:")
print(H)


# ============================================================
# 11. WARP POSTER INTO CAMERA IMAGE
# ============================================================

warped_poster = cv2.warpPerspective(
    poster,
    H,
    (
        image.shape[1],
        image.shape[0]
    )
)


# ============================================================
# 12. CREATE MASK FOR THE POSTER
# ============================================================

mask = np.zeros(
    image.shape[:2],
    dtype=np.uint8
)

cv2.fillConvexPoly(
    mask,
    np.int32(expanded_corners),
    255
)


# ============================================================
# 13. REMOVE THE ORIGINAL AREA WHERE POSTER WILL GO
# ============================================================

inverse_mask = cv2.bitwise_not(mask)

background = cv2.bitwise_and(
    image,
    image,
    mask=inverse_mask
)


# ============================================================
# 14. EXTRACT THE WARPED POSTER
# ============================================================

poster_area = cv2.bitwise_and(
    warped_poster,
    warped_poster,
    mask=mask
)


# ============================================================
# 15. COMBINE ORIGINAL IMAGE + POSTER
# ============================================================

augmented_image = cv2.add(
    background,
    poster_area
)


# ============================================================
# 16. SAVE FINAL AUGMENTED IMAGE
# ============================================================

output_path = os.path.join(
    OUTPUT_FOLDER,
    "step2_AR_20221115_113319.jpg"
)

cv2.imwrite(
    output_path,
    augmented_image
)

print("\nFinal augmented image saved to:")
print(output_path)