import os

print(os.getcwd())
print(os.listdir())

from ultralytics import YOLO
import cv2

# Load the trained model only once
model = YOLO("models/best (1).pt")


def detect_objects(image_path):
    """
    Runs YOLO detection on the uploaded image.

    Returns:
        original_img
        detected_img
        pothole_count
        crack_count
        normal_count
    """

    # Read original image
    original_img = cv2.imread(image_path)

    # Run prediction
    results = model.predict(
        source=image_path,
        conf=0.10,
        iou=0.45
    )

    result = results[0]

    # Draw bounding boxes
    detected_img = result.plot()

    pothole_count = 0
    crack_count = 0
    normal_count = 0

    class_names = model.names

    # Count detections
    for cls in result.boxes.cls:
        label = class_names[int(cls)]

        if label == "Pothhole":
            pothole_count += 1

        elif label == "Crack":
            crack_count += 1

        elif label == "Normal Road":
            normal_count += 1

    return (
        original_img,
        detected_img,
        pothole_count,
        crack_count,
        normal_count
    )