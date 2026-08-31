import streamlit as st
import os
import cv2

from utils.detector import detect_objects

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Pothole Detection",
    page_icon="🛣️",
    layout="wide"
)

st.title("🛣️ Pothole Detection Using YOLO11")
st.write("Upload a road image to detect potholes and cracks.")

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
    original_img, detected_img, potholes, cracks, normal = detect_objects(image_path)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(
            cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB),
            use_container_width=True
        )

    with col2:
        st.subheader("Detected Image")
        st.image(
            cv2.cvtColor(detected_img, cv2.COLOR_BGR2RGB),
            use_container_width=True
        )

    st.divider()

    st.subheader("Detection Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric("🕳️ Potholes", potholes)
    c2.metric("🪨 Cracks", cracks)
    c3.metric("🛣️ Normal Road", normal)