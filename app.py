import streamlit as st
import os
from io import BytesIO
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

.stApp { background: radial-gradient(circle at 90% 0%, #263a32 0, #101715 42%, #0b0f0e 78%); }
.block-container { max-width: 1180px; padding: 2.5rem 2rem 4rem; }
h1, h2, h3, p, label, div { font-family: 'Space Grotesk', sans-serif; }
.topline { color: #d7f45b; font-family: 'DM Mono', monospace; font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; }
.topbar { align-items: flex-start; display: flex; justify-content: space-between; margin-bottom: .6rem; }
.creator { color: #eef2f0; font-family: 'DM Mono', monospace; font-size: .72rem; letter-spacing: .04em; text-align: right; }
.creator span { color: #9ca9a4; display: block; font-size: .62rem; margin-top: .25rem; }
.hero { border-bottom: 1px solid #2d3a36; margin: .8rem 0 2rem; padding-bottom: 2rem; }
.hero h1 { color: #eef2f0; font-size: clamp(2.8rem, 7vw, 5.8rem); letter-spacing: -.05em; line-height: .92; margin: 0; }
.hero h1 span { color: #d7f45b; }
.hero p { color: #9ca9a4; font-size: 1.05rem; margin: 1.3rem 0 0; max-width: 560px; }
.panel { background: rgba(23, 32, 30, .82); border: 1px solid #2d3a36; border-radius: 8px; padding: 1.25rem; }
.panel-label { color: #ff9d58; font-family: 'DM Mono', monospace; font-size: .7rem; letter-spacing: .12em; text-transform: uppercase; }
.status-card { border: 1px solid #466247; border-radius: 8px; background: linear-gradient(135deg, #293b2d, #17221d); padding: 1.2rem 1.35rem; }
.status-label { color: #9ca9a4; font-family: 'DM Mono', monospace; font-size: .7rem; text-transform: uppercase; }
.status-value { font-size: 2rem; font-weight: 700; line-height: 1.1; margin: .4rem 0; }
.status-copy { color: #9ca9a4; font-size: .84rem; }
.section-label { color: #ff9d58; font-family: 'DM Mono', monospace; font-size: .7rem; letter-spacing: .12em; margin: 2rem 0 .8rem; text-transform: uppercase; }
.image-label { color: #9ca9a4; font-family: 'DM Mono', monospace; font-size: .7rem; letter-spacing: .1em; margin-bottom: .6rem; text-transform: uppercase; }
.stFileUploader { background: transparent; border: 1px dashed #52635c; border-radius: 6px; }
.stImage img { border: 1px solid #2d3a36; border-radius: 6px; }
[data-testid="stMetric"] { background: #17201e; border: 1px solid #2d3a36; border-radius: 6px; padding: .8rem; }
[data-testid="stMetricValue"] { color: #d7f45b; }
.stProgress > div > div > div > div { background: #d7f45b; }
hr { border-color: #2d3a36; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div class="topline">Road intelligence / live field dashboard</div>
    <div class="creator">Created by NARESH<span>727824tuam029</span></div>
</div>
<section class="hero">
    <h1>Read the road<br><span>before it breaks.</span></h1>
    <p>Upload a road image to identify potholes, cracks, and clear pavement with YOLO11 computer vision.</p>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="panel"><div class="panel-label">01 / Upload inspection image</div>', unsafe_allow_html=True)

# -------------------------------
# Upload Image
# -------------------------------

uploaded_file = st.file_uploader(
    "Drop a road image here",
    type=["jpg", "jpeg", "png"]
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:

    # Create uploads folder if not present
    os.makedirs("uploads", exist_ok=True)

    image_path = os.path.join("uploads", uploaded_file.name)

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Image uploaded. Analysis complete.")

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
    hazard_scores = [
        item["Probability"] * (1.0 if item["Class"] == "Pothhole" else 0.65)
        for item in predictions
        if item["Class"] in {"Pothhole", "Crack"}
    ]
    accident_probability = min(
        1.0,
        max(hazard_scores, default=0) + max(0, len(hazard_scores) - 1) * 0.05
    )
    if potholes:
        status = "HIGH RISK"
        status_color = "#ff6b5f"
        status_copy = "Pothole regions need attention."
    elif cracks:
        status = "REVIEW"
        status_color = "#ffb454"
        status_copy = "Crack regions detected for review."
    else:
        status = "CLEAR"
        status_color = "#76e39a"
        status_copy = "No road defects detected in this frame."

    st.markdown('<div class="section-label">02 / Probability status</div>', unsafe_allow_html=True)
    status_col, total_col, average_col, peak_col, accident_col = st.columns(5)
    status_col.markdown(
        f"<div class='status-card'><div class='status-label'>Road condition</div><div class='status-value' style='color:{status_color}'>{status}</div><div class='status-copy'>{status_copy}</div></div>",
        unsafe_allow_html=True
    )
    total_col.metric("Predictions", total_predictions)
    average_col.metric("Average probability", f"{average_probability:.1%}")
    peak_col.metric("Highest probability", f"{highest_probability:.1%}")
    accident_col.metric("Accident probability", f"{accident_probability:.1%}")
    st.progress(accident_probability, text=f"Estimated accident probability · {accident_probability:.1%}")

    st.caption(
        f"Scan completed {datetime.now().strftime('%d %b %Y, %H:%M:%S')} · "
        f"{hazard_predictions} road issue(s) detected"
    )
    st.caption("Accident probability is an estimate based on detected hazard confidence, not a calibrated safety statistic.")

    st.markdown('<div class="section-label">03 / Visual evidence</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="image-label">Source frame</div>', unsafe_allow_html=True)
        st.image(original_img, use_container_width=True)

    with col2:
        st.markdown('<div class="image-label">Annotated prediction</div>', unsafe_allow_html=True)
        st.image(detected_img, use_container_width=True)
        download_buffer = BytesIO()
        detected_img.save(download_buffer, format="PNG")
        st.download_button(
            "Download annotated image",
            data=download_buffer.getvalue(),
            file_name="pothole_detection_result.png",
            mime="image/png",
            use_container_width=True,
        )

    st.markdown('<div class="section-label">04 / Detection summary</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    c1.metric("🕳️ Potholes", potholes)
    c2.metric("🪨 Cracks", cracks)
    c3.metric("🛣️ Normal Road", normal)

    st.markdown('<div class="section-label">05 / Prediction graph</div>', unsafe_allow_html=True)
    if predictions:
        chart_data = {
            f"{index + 1}. {item['Class']}": item["Probability"]
            for index, item in enumerate(predictions)
        }
        st.bar_chart(chart_data, horizontal=True, y_label="Detection", x_label="Probability")
        st.caption("Each bar represents the model confidence for one detected region.")
        st.caption("Confidence guide: 90%+ strong signal · 60-89% review · below 60% low signal")
    else:
        st.info("No objects were detected in this image.")

    st.markdown('<div class="section-label">06 / Prediction details</div>', unsafe_allow_html=True)
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