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

    st.markdown('<div class="result-heading">Detection summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-panel">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    c1.metric("Potholes", potholes)
    c2.metric("Cracks", cracks)
    c3.metric("Clear road", normal)
    st.markdown('</div>', unsafe_allow_html=True)