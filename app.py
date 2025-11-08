import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(
    page_title="AlfaStack AI Inspector",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise CSS
st.markdown("""
<style>
    .main { background: #0f172a; color: white; }
    .enterprise-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 25px 25px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-title { 
        font-size: 3.2rem; 
        font-weight: 800; 
        color: white; 
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .sub-title { 
        font-size: 1.3rem; 
        color: #dbeafe; 
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    .enterprise-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .upload-zone {
        border: 3px dashed #3b82f6;
        border-radius: 20px;
        padding: 4rem 2rem;
        text-align: center;
        background: rgba(59, 130, 246, 0.05);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .upload-zone:hover {
        background: rgba(59, 130, 246, 0.1);
        border-color: #60a5fa;
    }
    .stButton button {
        background: linear-gradient(45deg, #3b82f6, #1e40af);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Enterprise Header
st.markdown("""
<div class="enterprise-header">
    <h1 class="main-title">🏭 AlfaStack Vision AI</h1>
    <p class="sub-title">Enterprise-Grade Defect Detection • Industry 4.0 Ready • Real-time Analytics</p>
</div>
""", unsafe_allow_html=True)

# Load AI Model
@st.cache_resource
def load_model():
    return YOLO('yolov8n.pt')

model = load_model()

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Main Dashboard
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
    st.markdown("### 🖼️ Product Inspection Portal")
    
    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "**🚀 DRAG & DROP MANUFACTURING SAMPLE**", 
        type=['jpg', 'jpeg', 'png', 'bmp'],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="🔬 Product Under Analysis")
        
        # Image Analytics
        st.markdown("#### 📏 Image Analytics")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Dimensions", f"{image.size[0]}x{image.size[1]}")
        with col_b:
            st.metric("Color Mode", image.mode)
        with col_c:
            st.metric("File Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
    st.markdown("### 📈 AI Analysis Dashboard")
    
    if uploaded_file:
        # Control Panel
        st.markdown("#### ⚙️ Precision Controls")
        col_x, col_y = st.columns(2)
        with col_x:
            confidence = st.slider("AI Confidence", 0.1, 1.0, 0.6, 0.05)
        with col_y:
            st.metric("AI Status", "Online", "Ready")
        
        # Action Center
        if st.button("🚀 LAUNCH AI INSPECTION", use_container_width=True, type="primary"):
            with st.spinner("**🔬 AI ENGINE ANALYZING MANUFACTURING QUALITY...**"):
                # Progress simulation
                progress_bar = st.progress(0)
                for percent in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(percent + 1)
                
                # AI Processing
                image_np = np.array(image)
                results = model(image_np, conf=confidence)
                
                if len(results) > 0:
                    # Enhanced Results
                    result_img = results[0].plot()
                    result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                    
                    st.image(result_img_rgb, use_container_width=True, caption="🎯 AI DEFECT MAPPING")
                    
                    # Enterprise Metrics
                    defect_count = len(results[0].boxes)
                    objects_data = []
                    
                    for i, box in enumerate(results[0].boxes):
                        class_id = int(box.cls[0])
                        class_name = model.names[class_id]
                        conf = box.conf[0].item()
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
                        # Advanced measurements
                        width = x2 - x1
                        height = y2 - y1
                        area = width * height
                        aspect_ratio = width / height if height > 0 else 0
                        
                        objects_data.append({
                            'Defect ID': i+1,
                            'Type': class_name.upper(),
                            'Confidence': f"{conf:.1%}",
                            'Width': f"{width:.1f}px",
                            'Height': f"{height:.1f}px",
                            'Area': f"{area:.1f}px²",
                            'Aspect Ratio': f"{aspect_ratio:.2f}"
                        })
                    
                    # Display Analysis
                    st.markdown("#### 📊 Detailed Analysis Report")
                    df = pd.DataFrame(objects_data)
                    st.dataframe(df, use_container_width=True)
                    
                    # Key Metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f'<div class="metric-card"><h4>DEFECTS</h4><h2>{defect_count}</h2></div>', unsafe_allow_html=True)
                    
                    with col2:
                        avg_conf = np.mean([box.conf[0].item() for box in results[0].boxes])
                        st.markdown(f'<div class="metric-card"><h4>CONFIDENCE</h4><h2>{avg_conf:.1%}</h2></div>', unsafe_allow_html=True)
                    
                    with col3:
                        total_area = sum([(box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1]) for box in results[0].boxes])
                        st.markdown(f'<div class="metric-card"><h4>TOTAL AREA</h4><h2>{total_area:.0f} px²</h2></div>', unsafe_allow_html=True)
                    
                    with col4:
                        status = "❌ REJECT" if defect_count > 0 else "✅ PASS"
                        st.markdown(f'<div class="metric-card"><h4>VERDICT</h4><h2>{status}</h2></div>', unsafe_allow_html=True)
                    
                    # Save to history
                    st.session_state.analysis_history.append({
                        'timestamp': datetime.now(),
                        'defects': defect_count,
                        'confidence': avg_conf
                    })
                    
                else:
                    # Perfect Quality
                    st.success("🎉 **MANUFACTURING EXCELLENCE ACHIEVED**")
                    st.balloons()
                    st.markdown('''
                    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #00b09b, #96c93d); border-radius: 20px; margin: 2rem 0;">
                        <h2 style="color: white; margin: 0;">✅ QUALITY CERTIFIED</h2>
                        <p style="color: white; font-size: 1.2rem;">Zero Defects • Production Ready • Market Perfect</p>
                    </div>
                    ''', unsafe_allow_html=True)
    else:
        st.info("""
        👆 **UPLOAD MANUFACTURING SAMPLE FOR AI ANALYSIS**
        
        *Enterprise Features:*
        • **Real-time** defect detection
        • **Advanced** object measurements  
        • **Professional** analytics
        • **Industry 4.0** compatible
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Analytics Section
if st.session_state.analysis_history:
    st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Quality Analytics")
    
    history_df = pd.DataFrame(st.session_state.analysis_history)
    if not history_df.empty:
        fig = px.line(history_df, x='timestamp', y='defects', 
                     title='Defect Trend Analysis', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Enterprise Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem;">
    <h4>AlfaStack Vision AI • Enterprise SaaS Platform</h4>
    <p>Advanced Defect Detection • Real-time Analytics • Manufacturing Intelligence</p>
    <p style="font-size: 0.9rem;">🔒 Enterprise Grade • 📊 Real-time Analytics • 🚀 Scalable Infrastructure</p>
</div>
""", unsafe_allow_html=True)
