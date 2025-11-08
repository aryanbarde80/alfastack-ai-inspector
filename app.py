import streamlit as st
import numpy as np
from PIL import Image
from ultralytics import YOLO
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="AlfaStack AI",
    page_icon="🏭",
    layout="wide"
)

st.markdown("""
<style>
    .main { background: #0f172a; color: white; }
    .header { background: #1e3a8a; padding: 2rem; text-align: center; }
    .card { background: #1e293b; padding: 2rem; border-radius: 10px; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>🏭 AlfaStack AI Inspector</h1>
    <p>Enterprise Defect Detection</p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return YOLO('yolov8n.pt')

model = load_model()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📤 Upload Image")
    uploaded_file = st.file_uploader("", type=['jpg','png'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

with col2:
    st.markdown("### 📊 Results")
    if uploaded_file:
        if st.button("🔍 Detect Defects", type="primary"):
            with st.spinner("Analyzing..."):
                image_np = np.array(image)
                results = model(image_np)
                if len(results) > 0:
                    result_img = results[0].plot()
                    st.image(result_img, use_container_width=True)
                    defect_count = len(results[0].boxes)
                    st.success(f"Found {defect_count} defects!")
                    for i, box in enumerate(results[0].boxes):
                        class_id = int(box.cls[0])
                        class_name = model.names[class_id]
                        conf = box.conf[0].item()
                        st.write(f"{i+1}. {class_name} ({conf:.2f})")
                else:
                    st.success("✅ No defects found!")
