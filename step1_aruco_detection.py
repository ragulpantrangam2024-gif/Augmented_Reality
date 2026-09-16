import cv2
import os


# ============================================================
# STEP 1: ARUCO MARKER DETECTION
# Computer Vision - Augmented Reality
# ============================================================


# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

# Get the folder where this Python script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dataset folder
INPUT_FOLDER = os.path.join(
    BASE_DIR,
    "dataset"
)

# Results folder
OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "results"
)

# Create results folder if it doesn't exist
os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# ------------------------------------------------------------
# 2. PRINT PROJECT INFORMATION
# ------------------------------------------------------------

print("=" * 60)
print("ARUCO MARKER DETECTION")
print("=" * 60)

print("Project folder:")
print(BASE_DIR)

print()

print("Dataset folder:")
print(INPUT_FOLDER)

print()

print("Results folder:")
print(OUTPUT_FOLDER)

print()


# ------------------------------------------------------------
# 3. CHECK DATASET FOLDER
# ------------------------------------------------------------

if not os.path.exists(INPUT_FOLDER):

    print("ERROR: Dataset folder does not exist!")
    print()
    print("Expected location:")
    print(INPUT_FOLDER)

    input("\nPress Enter to exit...")
    exit()


# ------------------------------------------------------------
# 4. FIND IMAGES
# ------------------------------------------------------------

# Only accept actual image files.
# Using os.listdir() avoids duplicate matches on Windows.

image_paths = []

for filename in os.listdir(INPUT_FOLDER):

    # Convert extension to lowercase
    extension = os.path.splitext(
        filename
    )[1].lower()

    # Supported image formats
    if extension in [
        ".jpg",
        ".jpeg",
        ".png"
    ]:

        image_path = os.path.join(
            INPUT_FOLDER,
            filename
        )

        image_paths.append(
            image_path
        )


# Sort images alphabetically
image_paths.sort()


# ------------------------------------------------------------
# 5. DATASET INFORMATION
# ------------------------------------------------------------

print(
    f"Number of images found: "
    f"{len(image_paths)}"
)

print()

if len(image_paths) == 0:

    print(
        "ERROR: No image files were found "
        "inside the dataset folder."
    )

    print()
    print("Dataset contents:")

    for item in os.listdir(INPUT_FOLDER):
        print("   ", item)

    input("\nPress Enter to exit...")
    exit()


# Print filenames
print("Images to be processed:")

for index, image_path in enumerate(
    image_paths,
    start=1
):

    print(
        f"{index:02d}. "
        f"{os.path.basename(image_path)}"
    )

print()


# ------------------------------------------------------------
# 6. CREATE ARUCO DICTIONARY
# ------------------------------------------------------------

# The marker in our dataset uses the
# 6x6 ArUco dictionary.

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_6X6_50
)


# ------------------------------------------------------------
# 7. CREATE DETECTOR PARAMETERS
# ------------------------------------------------------------

parameters = cv2.aruco.DetectorParameters()


# ------------------------------------------------------------
# 8. CREATE ARUCO DETECTOR
# ------------------------------------------------------------

detector = cv2.aruco.ArucoDetector(
    ARUCO_DICT,
    parameters
)


# ------------------------------------------------------------
# 9. DETECTION COUNTERS
# ------------------------------------------------------------

detected_count = 0
failed_count = 0


# ------------------------------------------------------------
# 10. PROCESS EVERY IMAGE
# ------------------------------------------------------------

for image_number, image_path in enumerate(
    image_paths,
    start=1
):

    print("-" * 60)

    filename = os.path.basename(
        image_path
    )

    print(
        f"Image {image_number}/"
        f"{len(image_paths)}: "
        f"{filename}"
    )


    # --------------------------------------------------------
    # Read image
    # --------------------------------------------------------

    image = cv2.imread(
        image_path
    )


    if image is None:

        print(
            "ERROR: Could not read image."
        )

        failed_count += 1

        continue


    # Create a copy for drawing
    output = image.copy()


    # --------------------------------------------------------
    # Detect ArUco markers
    # --------------------------------------------------------

    corners, ids, rejected = detector.detectMarkers(
        image
    )


    # --------------------------------------------------------
    # Check detection
    # --------------------------------------------------------

    if ids is None:

        print(
            "Marker detected: NO"
        )

        print(
            f"Rejected candidates: "
            f"{len(rejected)}"
        )

        failed_count += 1


        # Save image
        output_path = os.path.join(
            OUTPUT_FOLDER,
            "detected_" + filename
        )

        cv2.imwrite(
            output_path,
            output
        )

        print(
            f"Saved: {output_path}"
        )

        continue


    # --------------------------------------------------------
    # Marker detected
    # --------------------------------------------------------

    detected_count += 1

    print(
        "Marker detected: YES"
    )

    print(
        f"Number of markers: "
        f"{len(ids)}"
    )

    print(
        f"Marker IDs: "
        f"{ids.flatten().tolist()}"
    )


    # --------------------------------------------------------
    # Draw detected markers
    # --------------------------------------------------------

    cv2.aruco.drawDetectedMarkers(
        output,
        corners,
        ids
    )


    # --------------------------------------------------------
    # Process each detected marker
    # --------------------------------------------------------

    for marker_index, marker_id in enumerate(
        ids.flatten()
    ):

        # ----------------------------------------------------
        # Extract four corners
        # ----------------------------------------------------

        marker_corners = corners[
            marker_index
        ][0]


        # ArUco corner order:
        #
        # 0 -> Top-left
        # 1 -> Top-right
        # 2 -> Bottom-right
        # 3 -> Bottom-left

        top_left = marker_corners[0]

        top_right = marker_corners[1]

        bottom_right = marker_corners[2]

        bottom_left = marker_corners[3]


        # ----------------------------------------------------
        # Print corner coordinates
        # ----------------------------------------------------

        print()

        print(
            f"Marker ID: {marker_id}"
        )

        print(
            f"Top-left:     "
            f"({top_left[0]:.2f}, "
            f"{top_left[1]:.2f})"
        )

        print(
            f"Top-right:    "
            f"({top_right[0]:.2f}, "
            f"{top_right[1]:.2f})"
        )

        print(
            f"Bottom-right: "
            f"({bottom_right[0]:.2f}, "
            f"{bottom_right[1]:.2f})"
        )

        print(
            f"Bottom-left:  "
            f"({bottom_left[0]:.2f}, "
            f"{bottom_left[1]:.2f})"
        )


        # ----------------------------------------------------
        # Draw corner labels
        # ----------------------------------------------------

        corner_points = [
            (top_left, "TL"),
            (top_right, "TR"),
            (bottom_right, "BR"),
            (bottom_left, "BL")
        ]


        for point, label in corner_points:

            x = int(point[0])
            y = int(point[1])


            # Draw point
            cv2.circle(
                output,
                (x, y),
                8,
                (0, 255, 0),
                -1
            )


            # Draw label
            cv2.putText(
                output,
                label,
                (x + 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )


        # ----------------------------------------------------
        # Calculate marker center
        # ----------------------------------------------------

        center_x = int(
            (
                top_left[0]
                + bottom_right[0]
            ) / 2
        )

        center_y = int(
            (
                top_left[1]
                + bottom_right[1]
            ) / 2
        )


        # ----------------------------------------------------
        # Display marker ID
        # ----------------------------------------------------

        cv2.putText(
            output,
            f"ID: {marker_id}",
            (
                center_x - 40,
                center_y
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )


    # --------------------------------------------------------
    # Save annotated image
    # --------------------------------------------------------

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "detected_" + filename
    )

    cv2.imwrite(
        output_path,
        output
    )

    print()

    print(
        f"Saved: {output_path}"
    )


# ------------------------------------------------------------
# 11. FINAL SUMMARY
# ------------------------------------------------------------

print()
print("=" * 60)
print("DETECTION COMPLETED")
print("=" * 60)

print(
    f"Total images:     {len(image_paths)}"
)

print(
    f"Marker detected:  {detected_count}"
)

print(
    f"Marker not found: {failed_count}"
)

print()

print(
    "Results saved in:"
)

print(
    OUTPUT_FOLDER
)

print("=" * 60)