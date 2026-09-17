import cv2
import os


# --------------------------------------------------
# 1. Project folders
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FOLDER = os.path.join(BASE_DIR, "my_dataset")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "results")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# --------------------------------------------------
# 2. Dictionaries to test
# --------------------------------------------------

dictionaries = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
}


# --------------------------------------------------
# 3. Find images
# --------------------------------------------------

image_files = []

for filename in os.listdir(INPUT_FOLDER):

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_files.append(filename)

image_files.sort()


print("Number of images found:", len(image_files))
print()


# --------------------------------------------------
# 4. Test every dictionary
# --------------------------------------------------

for filename in image_files:

    image_path = os.path.join(INPUT_FOLDER, filename)

    image = cv2.imread(image_path)

    if image is None:
        print("Could not read:", filename)
        continue

    print("--------------------------------------")
    print("Image:", filename)

    found = False

    for dict_name, dict_id in dictionaries.items():

        aruco_dict = cv2.aruco.getPredefinedDictionary(dict_id)

        parameters = cv2.aruco.DetectorParameters()

        detector = cv2.aruco.ArucoDetector(
            aruco_dict,
            parameters
        )

        corners, ids, rejected = detector.detectMarkers(image)

        if ids is not None:

            print("FOUND!")
            print("Dictionary:", dict_name)
            print("Marker ID:", ids.flatten())

            for marker_corners in corners:

                points = marker_corners[0]

                print("Corners:")

                for i, point in enumerate(points):
                    x, y = point
                    print(f"  Corner {i}: ({x:.1f}, {y:.1f})")

            # Draw detection
            cv2.aruco.drawDetectedMarkers(
                image,
                corners,
                ids
            )

            output_path = os.path.join(
                OUTPUT_FOLDER,
                "my_detection_" + filename
            )

            cv2.imwrite(output_path, image)

            found = True
            break

    if not found:
        print("No dictionary recognized the marker.")


print()
print("Dictionary test finished.")