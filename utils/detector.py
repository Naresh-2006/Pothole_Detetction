from pathlib import Path

from ultralytics import YOLO
from PIL import Image

# Load the trained model only once
MODEL_PATH = Path(__file__).resolve().parent.parent / "best.pt"
model = YOLO(str(MODEL_PATH))


def detect_objects(image_path):
    """
    Runs YOLO detection on the uploaded image.

    Returns:
        original_img
        detected_img
        pothole_count
        crack_count
        normal_count
        predictions
    """

    # Read original image
    original_img = Image.open(image_path).convert("RGB")

    # Run prediction
    results = model.predict(
        source=image_path,
        conf=0.10,
        iou=0.45
    )

    result = results[0]

    # Draw bounding boxes
    detected_img = Image.fromarray(result.plot()[:, :, ::-1])

    pothole_count = 0
    crack_count = 0
    normal_count = 0
    predictions = []

    class_names = model.names

    # Count detections
    for index, cls in enumerate(result.boxes.cls):
        label = class_names[int(cls)]
        confidence = float(result.boxes.conf[index])
        coordinates = [round(value, 1) for value in result.boxes.xyxy[index].tolist()]
        predictions.append({
            "Class": label,
            "Probability": confidence,
            "Confidence": f"{confidence:.1%}",
            "Box": coordinates,
        })

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
        normal_count,
        predictions
    )
