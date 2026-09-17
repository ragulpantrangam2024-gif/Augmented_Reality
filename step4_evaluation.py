import cv2
import numpy as np
import os
import math
import csv


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder containing the augmented images
INPUT_FOLDER = os.path.join(BASE_DIR, "results")

# Folder where evaluation images and results will be saved
OUTPUT_FOLDER = os.path.join(BASE_DIR, "results", "evaluation")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================
# GLOBAL VARIABLES FOR MOUSE SELECTION
# ============================================================

selected_points = []
current_image = None
display_image = None

display_scale = 1.0


# ============================================================
# MOUSE CALLBACK
# ============================================================

def mouse_callback(event, x, y, flags, param):
    global selected_points
    global display_scale

    if event == cv2.EVENT_LBUTTONDOWN:

        # Convert displayed coordinates back to original image coordinates
        original_x = int(x / display_scale)
        original_y = int(y / display_scale)

        selected_points.append((original_x, original_y))

        print(
            f"Point {len(selected_points)}: "
            f"({original_x}, {original_y})"
        )


# ============================================================
# DISPLAY IMAGE WITH SCALING
# ============================================================

def prepare_display(image):
    """
    Resize image only for displaying on the screen.

    The original image is NOT modified.
    Mouse coordinates are converted back to original coordinates.
    """

    global display_scale

    height, width = image.shape[:2]

    # Maximum display size
    max_width = 1600
    max_height = 900

    scale_x = max_width / width
    scale_y = max_height / height

    display_scale = min(scale_x, scale_y, 1.0)

    if display_scale < 1.0:

        new_width = int(width * display_scale)
        new_height = int(height * display_scale)

        display = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

    else:
        display = image.copy()

    return display


# ============================================================
# SELECT POINTS
# ============================================================

def select_points(image, number_of_points, instruction):
    """
    Let the user select a fixed number of points.
    Press ENTER after selecting all points.
    """

    global selected_points
    global display_image

    selected_points = []

    display_image = image.copy()

    cv2.namedWindow("Evaluation", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Evaluation", mouse_callback)

    while True:

        # Create fresh display image
        display = prepare_display(display_image)

        # Instruction text
        cv2.putText(
            display,
            instruction,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
            cv2.LINE_AA
        )

        # Draw selected points
        for i, point in enumerate(selected_points):

            x = int(point[0] * display_scale)
            y = int(point[1] * display_scale)

            cv2.circle(
                display,
                (x, y),
                7,
                (0, 0, 255),
                -1
            )

            cv2.putText(
                display,
                str(i + 1),
                (x + 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )

        cv2.imshow("Evaluation", display)

        key = cv2.waitKey(20) & 0xFF

        # ENTER
        if key == 13:

            if len(selected_points) == number_of_points:
                break

            print(
                f"\nPlease select exactly "
                f"{number_of_points} points."
            )

        # ESC
        elif key == 27:

            print("\nEvaluation cancelled.")

            cv2.destroyWindow("Evaluation")

            return None

    cv2.destroyWindow("Evaluation")

    return selected_points.copy()


# ============================================================
# CALCULATE LINE ANGLE
# ============================================================

def calculate_line_angle(point1, point2):
    """
    Calculate the angle of a line in degrees.

    0°   -> horizontal
    90°  -> vertical

    The angle is normalized to [-180°, 180°].
    """

    x1, y1 = point1
    x2, y2 = point2

    dx = x2 - x1
    dy = y2 - y1

    angle = math.degrees(math.atan2(dy, dx))

    return angle


# ============================================================
# ANGULAR DIFFERENCE
# ============================================================

def angular_difference(angle1, angle2):
    """
    Calculate the smallest difference between two LINE angles.

    A line has no direction, therefore:
    0° and 180° represent the same line.

    Result is between 0° and 90°.
    """

    difference = abs(angle1 - angle2)

    # Because a line is undirected
    difference = difference % 180

    if difference > 90:
        difference = 180 - difference

    return difference


# ============================================================
# CALCULATE POSTER EDGES
# ============================================================

def calculate_poster_edges(poster_points):
    """
    Poster points must be selected in this order:

        1. TL
        2. TR
        3. BR
        4. BL

    Geometry:

                 G2
          TL ----------- TR
          |              |
       G1 |              | G4
          |              |
          BL ----------- BR
                 G3
    """

    TL, TR, BR, BL = poster_points

    # Vertical edges
    G1 = (TL, BL)
    G4 = (TR, BR)

    # Horizontal edges
    G2 = (TL, TR)
    G3 = (BL, BR)

    return G1, G2, G3, G4


# ============================================================
# DRAW LINE
# ============================================================

def draw_line(image, point1, point2, label):

    p1 = tuple(map(int, point1))
    p2 = tuple(map(int, point2))

    cv2.line(
        image,
        p1,
        p2,
        (255, 0, 0),
        4
    )

    # Label position
    label_x = int((p1[0] + p2[0]) / 2)
    label_y = int((p1[1] + p2[1]) / 2)

    cv2.putText(
        image,
        label,
        (label_x, label_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 255),
        3,
        cv2.LINE_AA
    )


# ============================================================
# DRAW POINT
# ============================================================

def draw_point(image, point, label):

    x, y = map(int, point)

    cv2.circle(
        image,
        (x, y),
        8,
        (0, 0, 255),
        -1
    )

    cv2.putText(
        image,
        label,
        (x + 10, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
        cv2.LINE_AA
    )


# ============================================================
# EVALUATE ONE IMAGE
# ============================================================

def evaluate_image(image_path, image_number, total_images):

    print("\n")
    print("=" * 60)
    print(f"IMAGE {image_number}/{total_images}")
    print(os.path.basename(image_path))
    print("=" * 60)

    image = cv2.imread(image_path)

    if image is None:

        print("ERROR: Could not read image.")

        return None

    # --------------------------------------------------------
    # STEP 4.1
    # SELECT POSTER CORNERS
    # --------------------------------------------------------

    print("\nSTEP 4.1 - Select poster corners")

    print("Click:")
    print("TL -> TR -> BR -> BL")
    print("Then press ENTER.\n")

    poster_points = select_points(
        image,
        4,
        "Click poster: TL -> TR -> BR -> BL, then ENTER"
    )

    if poster_points is None:
        return None

    print("\nPoster points:")

    for i, point in enumerate(poster_points):

        labels = ["TL", "TR", "BR", "BL"]

        print(
            f"{labels[i]}: "
            f"({point[0]}, {point[1]})"
        )

    # --------------------------------------------------------
    # STEP 4.2
    # SELECT R1
    # --------------------------------------------------------

    print("\nSTEP 4.2 - Select reference line R1")

    print(
        "Click TWO points on a wall groove "
        "or another vertical reference."
    )

    print("Then press ENTER.\n")

    R1_points = select_points(
        image,
        2,
        "Select R1: vertical reference, then ENTER"
    )

    if R1_points is None:
        return None

    print("\nR1 points:")

    print(
        f"Point 1: "
        f"({R1_points[0][0]}, {R1_points[0][1]})"
    )

    print(
        f"Point 2: "
        f"({R1_points[1][0]}, {R1_points[1][1]})"
    )

    # --------------------------------------------------------
    # STEP 4.3
    # SELECT R2
    # --------------------------------------------------------

    print("\nSTEP 4.3 - Select reference line R2")

    print(
        "Click TWO points on the metal strip "
        "or another strong horizontal perspective line."
    )

    print("Then press ENTER.\n")

    R2_points = select_points(
        image,
        2,
        "Select R2: horizontal reference, then ENTER"
    )

    if R2_points is None:
        return None

    print("\nR2 points:")

    print(
        f"Point 1: "
        f"({R2_points[0][0]}, {R2_points[0][1]})"
    )

    print(
        f"Point 2: "
        f"({R2_points[1][0]}, {R2_points[1][1]})"
    )

    # ========================================================
    # GEOMETRY CALCULATION
    # ========================================================

    G1, G2, G3, G4 = calculate_poster_edges(
        poster_points
    )

    # Calculate angles
    G1_angle = calculate_line_angle(G1[0], G1[1])
    G2_angle = calculate_line_angle(G2[0], G2[1])
    G3_angle = calculate_line_angle(G3[0], G3[1])
    G4_angle = calculate_line_angle(G4[0], G4[1])

    R1_angle = calculate_line_angle(
        R1_points[0],
        R1_points[1]
    )

    R2_angle = calculate_line_angle(
        R2_points[0],
        R2_points[1]
    )

    # ========================================================
    # CORRECT COMPARISONS
    # ========================================================

    # Vertical edges compared with vertical reference
    G1_R1_error = angular_difference(
        G1_angle,
        R1_angle
    )

    G4_R1_error = angular_difference(
        G4_angle,
        R1_angle
    )

    # Horizontal edges compared with horizontal reference
    G2_R2_error = angular_difference(
        G2_angle,
        R2_angle
    )

    G3_R2_error = angular_difference(
        G3_angle,
        R2_angle
    )

    # ========================================================
    # AVERAGE ERRORS
    # ========================================================

    vertical_average_error = (
        G1_R1_error +
        G4_R1_error
    ) / 2

    horizontal_average_error = (
        G2_R2_error +
        G3_R2_error
    ) / 2

    overall_angular_difference = (
        G1_R1_error +
        G4_R1_error +
        G2_R2_error +
        G3_R2_error
    ) / 4

    # ========================================================
    # PRINT RESULTS
    # ========================================================

    print("\n")
    print("-" * 60)
    print("EVALUATION RESULTS")
    print("-" * 60)

    print(f"\nG1 angle: {G1_angle:.2f} deg")
    print(f"G2 angle: {G2_angle:.2f} deg")
    print(f"G3 angle: {G3_angle:.2f} deg")
    print(f"G4 angle: {G4_angle:.2f} deg")

    print(f"\nR1 angle: {R1_angle:.2f} deg")
    print(f"R2 angle: {R2_angle:.2f} deg")

    print("\nCorrect edge/reference comparisons:")

    print(
        f"G1 vs R1: "
        f"{G1_R1_error:.2f} deg"
    )

    print(
        f"G4 vs R1: "
        f"{G4_R1_error:.2f} deg"
    )

    print(
        f"G2 vs R2: "
        f"{G2_R2_error:.2f} deg"
    )

    print(
        f"G3 vs R2: "
        f"{G3_R2_error:.2f} deg"
    )

    print(
        f"\nVertical average error: "
        f"{vertical_average_error:.2f} deg"
    )

    print(
        f"Horizontal average error: "
        f"{horizontal_average_error:.2f} deg"
    )

    print(
        f"Overall angular difference: "
        f"{overall_angular_difference:.2f} deg"
    )

    # ========================================================
    # CREATE EVALUATION IMAGE
    # ========================================================

    evaluation_image = image.copy()

    # Draw poster corners
    labels = ["TL", "TR", "BR", "BL"]

    for point, label in zip(
        poster_points,
        labels
    ):
        draw_point(
            evaluation_image,
            point,
            label
        )

    # Draw poster edges
    draw_line(
        evaluation_image,
        G1[0],
        G1[1],
        "G1"
    )

    draw_line(
        evaluation_image,
        G2[0],
        G2[1],
        "G2"
    )

    draw_line(
        evaluation_image,
        G3[0],
        G3[1],
        "G3"
    )

    draw_line(
        evaluation_image,
        G4[0],
        G4[1],
        "G4"
    )

    # Draw reference lines
    cv2.line(
        evaluation_image,
        R1_points[0],
        R1_points[1],
        (0, 255, 0),
        5
    )

    cv2.line(
        evaluation_image,
        R2_points[0],
        R2_points[1],
        (0, 255, 0),
        5
    )

    # Reference labels
    R1_middle = (
        int((R1_points[0][0] + R1_points[1][0]) / 2),
        int((R1_points[0][1] + R1_points[1][1]) / 2)
    )

    R2_middle = (
        int((R2_points[0][0] + R2_points[1][0]) / 2),
        int((R2_points[0][1] + R2_points[1][1]) / 2)
    )

    cv2.putText(
        evaluation_image,
        "R1",
        R1_middle,
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        3,
        cv2.LINE_AA
    )

    cv2.putText(
        evaluation_image,
        "R2",
        R2_middle,
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        3,
        cv2.LINE_AA
    )

    # ========================================================
    # ADD RESULT TEXT
    # ========================================================

    result_lines = [

        f"G1 vs R1: {G1_R1_error:.2f} deg",

        f"G4 vs R1: {G4_R1_error:.2f} deg",

        f"G2 vs R2: {G2_R2_error:.2f} deg",

        f"G3 vs R2: {G3_R2_error:.2f} deg",

        f"Vertical avg: {vertical_average_error:.2f} deg",

        f"Horizontal avg: {horizontal_average_error:.2f} deg",

        f"Overall: {overall_angular_difference:.2f} deg"
    ]

    x_text = 30
    y_text = 40

    # Add a black rectangle behind text
    text_height = 40 * len(result_lines) + 20

    cv2.rectangle(
        evaluation_image,
        (10, 10),
        (520, text_height),
        (0, 0, 0),
        -1
    )

    for line in result_lines:

        cv2.putText(
            evaluation_image,
            line,
            (x_text, y_text),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        y_text += 40

    # ========================================================
    # SAVE EVALUATION IMAGE
    # ========================================================

    filename = os.path.basename(image_path)

    output_filename = (
        "evaluation_" +
        os.path.splitext(filename)[0] +
        ".jpg"
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    cv2.imwrite(
        output_path,
        evaluation_image
    )

    print("\nEvaluation image saved:")
    print(output_path)

    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {
        "image": filename,

        "G1_angle": G1_angle,
        "G2_angle": G2_angle,
        "G3_angle": G3_angle,
        "G4_angle": G4_angle,

        "R1_angle": R1_angle,
        "R2_angle": R2_angle,

        "G1_vs_R1": G1_R1_error,
        "G4_vs_R1": G4_R1_error,

        "G2_vs_R2": G2_R2_error,
        "G3_vs_R2": G3_R2_error,

        "vertical_average_error":
            vertical_average_error,

        "horizontal_average_error":
            horizontal_average_error,

        "overall_angular_difference":
            overall_angular_difference,

        "evaluation_image":
            output_path
    }


# ============================================================
# FIND INPUT IMAGES
# ============================================================

def find_input_images():

    image_extensions = (
        ".jpg",
        ".jpeg",
        ".png"
    )

    image_files = []

    for filename in os.listdir(INPUT_FOLDER):

        # Ignore the evaluation folder
        if filename.lower() == "evaluation":
            continue

        # Only image files
        if not filename.lower().endswith(
            image_extensions
        ):
            continue

        # We only want augmented evaluation images
        #
        # Examples:
        # AR_20221115_113319.jpg
        # FAILED_20221115_113635.jpg
        #
        # This avoids accidentally processing
        # detected_*.jpg or other intermediate images.

        if (
            filename.startswith("AR_") or
            filename.startswith("FAILED_")
        ):
            image_files.append(filename)

    # Sort alphabetically
    image_files.sort()

    return [
        os.path.join(INPUT_FOLDER, filename)
        for filename in image_files
    ]


# ============================================================
# SAVE CSV SUMMARY
# ============================================================

def save_csv(results):

    if not results:
        return

    csv_path = os.path.join(
        OUTPUT_FOLDER,
        "evaluation_summary.csv"
    )

    fieldnames = [
        "image",

        "G1_angle",
        "G2_angle",
        "G3_angle",
        "G4_angle",

        "R1_angle",
        "R2_angle",

        "G1_vs_R1",
        "G4_vs_R1",

        "G2_vs_R2",
        "G3_vs_R2",

        "vertical_average_error",
        "horizontal_average_error",

        "overall_angular_difference"
    ]

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for result in results:

            row = {
                key: result[key]
                for key in fieldnames
            }

            # Round numerical values
            for key in fieldnames:

                if key != "image":

                    row[key] = round(
                        row[key],
                        2
                    )

            writer.writerow(row)

    print("\nCSV summary saved:")
    print(csv_path)


# ============================================================
# SAVE TEXT SUMMARY
# ============================================================

def save_text_summary(results):

    if not results:
        return

    txt_path = os.path.join(
        OUTPUT_FOLDER,
        "evaluation_summary.txt"
    )

    with open(
        txt_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "STEP 4 - AUGMENTED REALITY EVALUATION\n"
        )

        file.write(
            "=" * 60 + "\n\n"
        )

        for index, result in enumerate(
            results,
            start=1
        ):

            file.write(
                f"IMAGE {index}\n"
            )

            file.write(
                f"{result['image']}\n\n"
            )

            file.write(
                f"G1 angle: "
                f"{result['G1_angle']:.2f} deg\n"
            )

            file.write(
                f"G2 angle: "
                f"{result['G2_angle']:.2f} deg\n"
            )

            file.write(
                f"G3 angle: "
                f"{result['G3_angle']:.2f} deg\n"
            )

            file.write(
                f"G4 angle: "
                f"{result['G4_angle']:.2f} deg\n"
            )

            file.write(
                f"R1 angle: "
                f"{result['R1_angle']:.2f} deg\n"
            )

            file.write(
                f"R2 angle: "
                f"{result['R2_angle']:.2f} deg\n\n"
            )

            file.write(
                f"G1 vs R1: "
                f"{result['G1_vs_R1']:.2f} deg\n"
            )

            file.write(
                f"G4 vs R1: "
                f"{result['G4_vs_R1']:.2f} deg\n"
            )

            file.write(
                f"G2 vs R2: "
                f"{result['G2_vs_R2']:.2f} deg\n"
            )

            file.write(
                f"G3 vs R2: "
                f"{result['G3_vs_R2']:.2f} deg\n\n"
            )

            file.write(
                f"Vertical average error: "
                f"{result['vertical_average_error']:.2f} deg\n"
            )

            file.write(
                f"Horizontal average error: "
                f"{result['horizontal_average_error']:.2f} deg\n"
            )

            file.write(
                f"Overall angular difference: "
                f"{result['overall_angular_difference']:.2f} deg\n"
            )

            file.write(
                "\n"
                + "-" * 60
                + "\n\n"
            )

    print("\nText summary saved:")
    print(txt_path)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("STEP 4 - AUGMENTED REALITY EVALUATION")
    print("=" * 60)

    print("\nInput folder:")
    print(INPUT_FOLDER)

    print("\nOutput folder:")
    print(OUTPUT_FOLDER)

    # --------------------------------------------------------
    # FIND IMAGES
    # --------------------------------------------------------

    image_paths = find_input_images()

    print(
        f"\nNumber of images found: "
        f"{len(image_paths)}"
    )

    if len(image_paths) == 0:

        print("\nNo AR images found.")

        print(
            "\nExpected files such as:"
        )

        print(
            "AR_20221115_113319.jpg"
        )

        print(
            "FAILED_20221115_113635.jpg"
        )

        return

    # --------------------------------------------------------
    # LIST IMAGES
    # --------------------------------------------------------

    print("\nImages:")

    for index, path in enumerate(
        image_paths,
        start=1
    ):

        print(
            f"{index}. "
            f"{os.path.basename(path)}"
        )

    print("\n")
    print(
        "For each image you will select:"
    )

    print(
        "1. Poster corners: TL -> TR -> BR -> BL"
    )

    print(
        "2. R1: vertical reference line"
    )

    print(
        "3. R2: horizontal reference line"
    )

    print(
        "\nPress ENTER after each selection."
    )

    print(
        "Press ESC during selection to stop."
    )

    # --------------------------------------------------------
    # EVALUATE ALL IMAGES
    # --------------------------------------------------------

    all_results = []

    for index, image_path in enumerate(
        image_paths,
        start=1
    ):

        result = evaluate_image(
            image_path,
            index,
            len(image_paths)
        )

        if result is None:

            print(
                "\nEvaluation stopped."
            )

            break

        all_results.append(result)

        print(
            "\nPress any key to continue "
            "to the next image."
        )

        cv2.waitKey(0)

    cv2.destroyAllWindows()

    # --------------------------------------------------------
    # SAVE SUMMARIES
    # --------------------------------------------------------

    save_csv(all_results)

    save_text_summary(all_results)

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60)

    print(
        f"\nImages evaluated: "
        f"{len(all_results)}"
    )

    if all_results:

        print("\nOverall angular differences:")

        for result in all_results:

            print(
                f"{result['image']}: "
                f"{result['overall_angular_difference']:.2f} deg"
            )

    print("\nResults are stored in:")
    print(OUTPUT_FOLDER)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()