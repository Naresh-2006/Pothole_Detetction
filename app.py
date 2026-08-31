import streamlit as st
import os
from datetime import datetime

from utils.detector import detect_objects

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Pothole Detection",
    page_icon="🛣️",
    layout="wide"
)

st.title("🛣️ Pothole Detection Dashboard")
st.write("Live road-condition analysis powered by YOLO11.")

st.divider()

# -------------------------------
# Upload Image
# -------------------------------

uploaded_file = st.file_uploader(
    "Choose an Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Create uploads folder if not present
    os.makedirs("uploads", exist_ok=True)

    image_path = os.path.join("uploads", uploaded_file.name)

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Image Uploaded Successfully!")

    # Run Detection
    original_img, detected_img, potholes, cracks, normal, predictions = detect_objects(image_path)

    total_predictions = len(predictions)
    hazard_predictions = potholes + cracks
    average_probability = (
        sum(item["Probability"] for item in predictions) / total_predictions
        if total_predictions else 0
    )
    highest_probability = max(
        (item["Probability"] for item in predictions),
        default=0
    )
    if potholes:
        status = "HIGH RISK"
        status_color = "#ff6b5f"
    elif cracks:
        status = "REVIEW"
        status_color = "#ffb454"
    else:
        status = "CLEAR"
        status_color = "#76e39a"

    st.markdown("---")
    st.subheader("Live prediction status")
    status_col, total_col, average_col, peak_col = st.columns(4)
    status_col.markdown(
        f"<h2 style='color:{status_color}; margin:0'>{status}</h2>",
        unsafe_allow_html=True
    )
    total_col.metric("Predictions", total_predictions)
    average_col.metric("Average probability", f"{average_probability:.1%}")
    peak_col.metric("Highest probability", f"{highest_probability:.1%}")

    st.caption(
        f"Scan completed {datetime.now().strftime('%d %b %Y, %H:%M:%S')} · "
        f"{hazard_predictions} road issue(s) detected"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(original_img, use_container_width=True)

    with col2:
        st.subheader("Detected Image")
        st.image(detected_img, use_container_width=True)

    st.divider()

    st.subheader("Detection Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric("🕳️ Potholes", potholes)
    c2.metric("🪨 Cracks", cracks)
    c3.metric("🛣️ Normal Road", normal)

    st.divider()
    st.subheader("Prediction probability graph")
    if predictions:
        chart_data = {
            f"{index + 1}. {item['Class']}": item["Probability"]
            for index, item in enumerate(predictions)
        }
        st.bar_chart(chart_data, horizontal=True, y_label="Detection", x_label="Probability")
        st.caption("Each bar represents the model confidence for one detected region.")
    else:
        st.info("No objects were detected in this image.")

    st.subheader("Prediction details")
    if predictions:
        st.dataframe(
            [
                {
                    "#": index + 1,
                    "Class": item["Class"],
                    "Confidence": item["Confidence"],
                    "Bounding box": str(item["Box"]),
                }
                for index, item in enumerate(predictions)
            ],
            use_container_width=True,
            hide_index=True,
        )