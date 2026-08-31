import streamlit as st
import os
import cv2

from utils.detector import detect_objects

st.set_page_config(
    page_title="Pothole Detection",
    page_icon="🛣",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --ink: #eef2f0;
    --muted: #9ca9a4;
    --panel: #17201e;
    --line: #2d3a36;
    --lime: #d7f45b;
    --orange: #ff9d58;
}

.stApp {
    background: radial-gradient(circle at 85% 0%, #263b32 0, #101615 38%, #0b0f0e 76%);
    color: var(--ink);
}

.block-container {
    max-width: 1180px;
    padding: 3.5rem 2rem 4rem;
}

h1, h2, h3, p, label, div {
    font-family: 'Space Grotesk', sans-serif;
}

.hero {
    border-bottom: 1px solid var(--line);
    padding: 0 0 2.6rem;
    margin-bottom: 2rem;
}

.eyebrow {
    color: var(--lime);
    font-family: 'DM Mono', monospace;
    font-size: .72rem;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero h1 {
    color: var(--ink);
    font-size: clamp(2.6rem, 6vw, 5.6rem);
    letter-spacing: -.055em;
    line-height: .95;
    margin: 0;
    max-width: 760px;
}

.hero h1 span { color: var(--lime); }

.hero-copy {
    color: var(--muted);
    font-size: 1.05rem;
    margin: 1.5rem 0 0;
    max-width: 540px;
}

.topbar {
    align-items: center;
    display: flex;
    justify-content: space-between;
    margin-bottom: 2.5rem;
}

.brand-mark {
    color: var(--ink);
    font-family: 'DM Mono', monospace;
    font-size: .78rem;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.creator-credit {
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-size: .68rem;
    letter-spacing: .04em;
    margin-top: .35rem;
}

.live-pill {
    border: 1px solid #4a654b;
    border-radius: 999px;
    color: var(--lime);
    font-family: 'DM Mono', monospace;
    font-size: .7rem;
    padding: .45rem .75rem;
    text-transform: uppercase;
}

.upload-panel, .metric-panel {
    background: rgba(23, 32, 30, .82);
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 1.25rem;
}

.panel-kicker {
    color: var(--orange);
    font-family: 'DM Mono', monospace;
    font-size: .72rem;
    letter-spacing: .1em;
    text-transform: uppercase;
}

.stFileUploader {
    background: transparent;
    border: 1px dashed #52635c;
    border-radius: 6px;
    margin-top: .8rem;
}

.stFileUploader section { padding: 1.2rem; }
.stFileUploader small { color: var(--muted); }

.status-line {
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-size: .78rem;
    margin-top: 1.1rem;
}

.status-dot {
    background: var(--lime);
    border-radius: 50%;
    display: inline-block;
    height: 8px;
    margin-right: 8px;
    width: 8px;
}

.result-heading {
    color: var(--ink);
    font-size: 1.45rem;
    font-weight: 600;
    margin: 2.3rem 0 1rem;
}

.section-label {
    color: var(--orange);
    font-family: 'DM Mono', monospace;
    font-size: .7rem;
    letter-spacing: .12em;
    margin: 2.2rem 0 .8rem;
    text-transform: uppercase;
}

.risk-panel {
    background: linear-gradient(135deg, #293b2d, #18251f);
    border: 1px solid #466247;
    border-radius: 8px;
    padding: 1.2rem 1.35rem;
}

.risk-title {
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-size: .7rem;
    letter-spacing: .1em;
    text-transform: uppercase;
}

.risk-value {
    color: var(--lime);
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1.1;
    margin: .45rem 0 .25rem;
}

.risk-copy { color: var(--muted); font-size: .88rem; }

.info-panel {
    background: rgba(23, 32, 30, .62);
    border-left: 2px solid var(--orange);
    padding: .8rem 1rem;
}

.info-panel p { color: var(--muted); font-size: .82rem; margin: .2rem 0; }
.info-panel strong { color: var(--ink); }

.stProgress > div > div > div > div { background-color: var(--lime); }

.image-label {
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-size: .72rem;
    letter-spacing: .1em;
    margin-bottom: .65rem;
    text-transform: uppercase;
}

.stImage img { border-radius: 6px; border: 1px solid var(--line); }

[data-testid="stMetric"] {
    background: transparent;
    border: 0;
    padding: .4rem .2rem;
}

[data-testid="stMetricLabel"] { color: var(--muted); }
[data-testid="stMetricValue"] { color: var(--lime); font-size: 2.3rem; }

hr { border-color: var(--line); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div>
        <div class="brand-mark">Pothole detection / field dashboard</div>
        <div class="creator-credit">Created by NARESH · 727824tuam029</div>
    </div>
    <div class="live-pill"><span class="status-dot"></span>Model online</div>
</div>
<section class="hero">
    <div class="eyebrow">Road intelligence / YOLO11 vision system</div>
    <h1>Read the road<br><span>before it breaks.</span></h1>
    <p class="hero-copy">Upload a road image for instant visual screening of potholes, cracks, and clear pavement.</p>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-panel"><div class="panel-kicker">01 / Inspect image</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop a road image here",
    type=["jpg", "jpeg", "png"]
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)

    image_path = os.path.join("uploads", uploaded_file.name)

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.markdown('<div class="status-line"><span class="status-dot"></span>Image received · running visual analysis</div>', unsafe_allow_html=True)
    original_img, detected_img, potholes, cracks, normal = detect_objects(image_path)

    total_detections = potholes + cracks + normal
    hazard_detections = potholes + cracks
    risk_ratio = hazard_detections / total_detections if total_detections else 0
    risk_level = "High attention" if risk_ratio >= 0.5 else "Review recommended" if hazard_detections else "Clear route"
    risk_copy = "Potential road defects detected" if hazard_detections else "No potholes or cracks detected"

    st.markdown('<div class="section-label">02 / Scan overview</div>', unsafe_allow_html=True)
    overview_col, detail_col = st.columns([1.2, 1], gap="large")
    with overview_col:
        st.markdown(f'''<div class="risk-panel"><div class="risk-title">Road condition signal</div><div class="risk-value">{risk_level}</div><div class="risk-copy">{risk_copy}</div></div>''', unsafe_allow_html=True)
    with detail_col:
        st.markdown(f'''<div class="info-panel"><p><strong>File</strong> {uploaded_file.name}</p><p><strong>Model</strong> YOLO11 road classifier</p><p><strong>Objects counted</strong> {total_detections}</p></div>''', unsafe_allow_html=True)

    st.markdown('<div class="section-label">03 / Detection metrics</div>', unsafe_allow_html=True)
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Total objects", total_detections)
    metric_col2.metric("Potholes", potholes)
    metric_col3.metric("Cracks", cracks)
    metric_col4.metric("Clear road", normal)

    st.markdown('<div class="result-heading">Visual comparison</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="image-label">Source frame</div>', unsafe_allow_html=True)
        st.image(
            cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB),
            use_container_width=True
        )

    with col2:
        st.markdown('<div class="image-label">Annotated output</div>', unsafe_allow_html=True)
        st.image(
            cv2.cvtColor(detected_img, cv2.COLOR_BGR2RGB),
            use_container_width=True
        )

    st.markdown('<div class="result-heading">Class distribution</div>', unsafe_allow_html=True)
    distribution_col, note_col = st.columns([1.4, 1], gap="large")
    with distribution_col:
        st.caption(f"{total_detections} object{'s' if total_detections != 1 else ''} identified in this frame")
        st.write("Potholes")
        st.progress(potholes / total_detections if total_detections else 0)
        st.write("Cracks")
        st.progress(cracks / total_detections if total_detections else 0)
        st.write("Clear road")
        st.progress(normal / total_detections if total_detections else 0)
    with note_col:
        st.markdown(f'''<div class="info-panel"><p><strong>Signal</strong></p><p>{risk_copy}. Use the annotated frame to locate each detected region.</p></div>''', unsafe_allow_html=True)