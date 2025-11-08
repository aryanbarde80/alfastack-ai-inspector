import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="AlfaStack Vision AI",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background: #0f172a; color: white; }
    .header { 
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
        padding: 3rem 2rem; border-radius: 0 0 25px 25px; text-align: center; 
        margin-bottom: 2rem;
    }
    .main-title { font-size: 3rem; font-weight: 800; color: white; margin: 0; }
    .sub-title { font-size: 1.2rem; color: #dbeafe; margin: 0.5rem 0 0 0; }
    .card { background: #1e293b; padding: 2rem; border-radius: 15px; border: 1px solid #334155; margin: 1rem 0; }
    .metric-card { background: #0f172a; padding: 1.5rem; border-radius: 10px; border: 1px solid #334155; text-align: center; }
    .upload-zone { border: 3px dashed #3b82f6; border-radius: 15px; padding: 3rem; text-align: center; background: rgba(59, 130, 246, 0.05); margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1 class="main-title">🏭 AlfaStack Vision AI</h1>
    <p class="sub-title">Enterprise Defect Detection Platform • Powered by Computer Vision</p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return YOLO('yolov8n.pt')

model = load_model()

if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📤 Upload Product Image")
    
    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drag & drop manufacturing sample", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        st.success("✅ Ready for AI analysis")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 AI Analysis Results")
    
    if uploaded_file:
        confidence = st.slider("Detection Confidence", 0.1, 1.0, 0.6)
        
        if st.button("🚀 Start AI Inspection", type="primary", use_container_width=True):
            with st.spinner("🔍 AI analyzing product quality..."):
                image_np = np.array(image)
                results = model(image_np, conf=confidence)
                
                if len(results) > 0:
                    result_img = results[0].plot()
                    st.image(result_img, use_container_width=True)
                    
                    defect_count = len(results[0].boxes)
                    objects_data = []
                    
                    for i, box in enumerate(results[0].boxes):
                        class_id = int(box.cls[0])
                        class_name = model.names[class_id]
                        conf = box.conf[0].item()
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
                        width = x2 - x1
                        height = y2 - y1
                        area = width * height
                        
                        objects_data.append({
                            'Object': i+1,
                            'Type': class_name,
                            'Confidence': f"{conf:.1%}",
                            'Width': f"{width:.1f}px",
                            'Height': f"{height:.1f}px",
                            'Area': f"{area:.1f}px²"
                        })
                    
                    df = pd.DataFrame(objects_data)
                    st.dataframe(df, use_container_width=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f'<div class="metric-card"><h4>Defects Found</h4><h2>{defect_count}</h2></div>', unsafe_allow_html=True)
                    with col2:
                        avg_conf = np.mean([box.conf[0].item() for box in results[0].boxes])
                        st.markdown(f'<div class="metric-card"><h4>Avg Confidence</h4><h2>{avg_conf:.1%}</h2></div>', unsafe_allow_html=True)
                    with col3:
                        status = "❌ REJECT" if defect_count > 0 else "✅ PASS"
                        st.markdown(f'<div class="metric-card"><h4>Verdict</h4><h2>{status}</h2></div>', unsafe_allow_html=True)
                    
                    st.session_state.analysis_history.append({
                        'timestamp': datetime.now(),
                        'defects': defect_count,
                        'image': uploaded_file.name
                    })
                else:
                    st.success("🎉 **Quality Certified** - No defects detected!")
    else:
        st.info("👆 Upload a product image to begin inspection")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b;'><p>AlfaStack Vision AI • Enterprise Quality Control</p></div>", unsafe_allow_html=True)
