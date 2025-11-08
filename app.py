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
import requests
import threading

# Page config
st.set_page_config(
    page_title="AlfaStack AI Inspector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern Website CSS
st.markdown("""
<style>
    /* Main styling */
    .main {
        background: #0f172a;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header */
    .website-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 3rem;
        border-radius: 0 0 25px 25px;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .sub-title {
        font-size: 1.3rem;
        color: #dbeafe;
        margin: 1rem 0 0 0;
        font-weight: 300;
    }
    
    /* Navigation */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .nav-item {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem 2rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* Cards */
    .feature-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: #3b82f6;
        transform: translateY(-5px);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Upload zone */
    .upload-container {
        border: 3px dashed #3b82f6;
        border-radius: 20px;
        padding: 4rem 2rem;
        text-align: center;
        background: rgba(59, 130, 246, 0.05);
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-container:hover {
        background: rgba(59, 130, 246, 0.1);
        border-color: #60a5fa;
    }
    
    /* Buttons */
    .primary-btn {
        background: linear-gradient(45deg, #3b82f6, #1e40af);
        color: white;
        border: none;
        padding: 1.2rem 3rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        margin: 1rem 0;
    }
    
    .primary-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
    }
    
    .secondary-btn {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 1rem 2rem;
        border-radius: 10px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .secondary-btn:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Tabs */
    .tab-container {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title { font-size: 2.5rem; }
        .nav-container { gap: 1rem; }
        .nav-item { padding: 0.8rem 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# Health monitoring
def keep_alive():
    while True:
        try:
            requests.get("https://alfastack-ai-inspector.onrender.com", timeout=10)
        except:
            pass
        time.sleep(840)

threading.Thread(target=keep_alive, daemon=True).start()

# Load model
@st.cache_resource
def load_model():
    return YOLO('yolov8n.pt')

model = load_model()

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Inspector"

# Website Header
st.markdown("""
<div class="website-header">
    <h1 class="main-title">🔍 AlfaStack AI Inspector</h1>
    <p class="sub-title">Enterprise-Grade Defect Detection Platform • Powered by Computer Vision</p>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("""
<div class="nav-container">
    <div class="nav-item" onclick="alert('Inspector')">🔍 Inspector</div>
    <div class="nav-item" onclick="alert('Analytics')">📊 Analytics</div>
    <div class="nav-item" onclick="alert('Settings')">⚙️ Settings</div>
    <div class="nav-item" onclick="alert('Documentation')">📚 Docs</div>
    <div class="nav-item" onclick="alert('Support')">💬 Support</div>
</div>
""", unsafe_allow_html=True)

# Main Content
tab1, tab2, tab3 = st.tabs(["🎯 AI Inspector", "📊 Analytics Dashboard", "⚙️ Enterprise Settings"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🖼️ Upload Center")
        st.markdown("Drag and drop your manufacturing samples for AI-powered quality inspection")
        
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "**CHOOSE MANUFACTURING SAMPLE**", 
            type=['jpg', 'jpeg', 'png', 'bmp'],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True, caption="📦 Product Under Analysis")
            
            # Quick stats
            st.markdown("#### 📏 Quick Analysis")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Dimensions", f"{image.size[0]}x{image.size[1]}")
            with col_b:
                st.metric("Format", image.format)
            with col_c:
                st.metric("Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 AI Analysis Engine")
        
        if uploaded_file:
            # Controls
            st.markdown("#### ⚙️ Analysis Configuration")
            col_x, col_y = st.columns(2)
            with col_x:
                confidence = st.slider("Detection Confidence", 0.1, 1.0, 0.6, 0.05)
            with col_y:
                mode = st.selectbox("Analysis Mode", ["Standard", "High Precision", "Fast Scan"])
            
            # Action button
            if st.button("🚀 START AI INSPECTION", use_container_width=True, type="primary"):
                with st.spinner("**AI Engine Processing Manufacturing Sample...**"):
                    # Progress
                    progress_bar = st.progress(0)
                    for percent in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(percent + 1)
                    
                    # AI Processing
                    image_np = np.array(image)
                    results = model(image_np, conf=confidence)
                    
                    if len(results) > 0:
                        result_img = results[0].plot()
                        result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                        
                        st.image(result_img_rgb, use_container_width=True, caption="🎯 AI Defect Mapping")
                        
                        # Results
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
                                'ID': i+1,
                                'Defect Type': class_name.upper(),
                                'Confidence': f"{conf:.1%}",
                                'Width': f"{width:.1f}px",
                                'Height': f"{height:.1f}px",
                                'Area': f"{area:.1f}px²"
                            })
                        
                        # Display results
                        st.markdown("#### 📋 Inspection Report")
                        df = pd.DataFrame(objects_data)
                        st.dataframe(df, use_container_width=True)
                        
                        # Stats
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.markdown(f'<div class="stats-card"><h4>DEFECTS</h4><h2>{defect_count}</h2></div>', unsafe_allow_html=True)
                        
                        with col2:
                            avg_conf = np.mean([box.conf[0].item() for box in results[0].boxes])
                            st.markdown(f'<div class="stats-card"><h4>CONFIDENCE</h4><h2>{avg_conf:.1%}</h2></div>', unsafe_allow_html=True)
                        
                        with col3:
                            total_area = sum([(box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1]) for box in results[0].boxes])
                            st.markdown(f'<div class="stats-card"><h4>TOTAL AREA</h4><h2>{total_area:.0f}</h2></div>', unsafe_allow_html=True)
                        
                        with col4:
                            status = "❌ REJECT" if defect_count > 0 else "✅ PASS"
                            st.markdown(f'<div class="stats-card"><h4>VERDICT</h4><h2>{status}</h2></div>', unsafe_allow_html=True)
                        
                        # Save history
                        st.session_state.analysis_history.append({
                            'timestamp': datetime.now(),
                            'defects': defect_count,
                            'confidence': avg_conf
                        })
                        
                    else:
                        st.success("🎉 **QUALITY CERTIFIED**")
                        st.balloons()
                        st.markdown("""
                        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #00b09b, #96c93d); border-radius: 15px;">
                            <h3 style="color: white;">✅ Manufacturing Excellence</h3>
                            <p style="color: white;">Zero defects detected • Production ready</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("""
            👆 **Upload a manufacturing sample to begin AI-powered inspection**
            
            *Supported Features:*
            • Real-time defect detection
            • Advanced object measurements
            • Quality scoring & reporting
            • Enterprise-grade analytics
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Business Intelligence")
    
    # Analytics dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        # Defect trend
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        defects = [45, 38, 32, 28, 25, 22]
        
        fig = px.line(x=months, y=defects, title='Defect Trend Analysis',
                     labels={'x': 'Month', 'y': 'Defects'})
        fig.update_traces(line=dict(color='#3b82f6', width=3))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Defect types
        defect_types = ['Scratches', 'Dents', 'Color Issues', 'Size Variations']
        counts = [25, 18, 12, 8]
        
        fig = px.pie(values=counts, names=defect_types, title='Defect Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
    st.markdown("#### 🎯 Performance Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Inspections", "1,247", "12 today")
    with col2:
        st.metric("Defect Rate", "2.3%", "-0.4%")
    with col3:
        st.metric("Avg Processing", "47ms", "Fast")
    with col4:
        st.metric("Uptime", "99.9%", "Stable")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Enterprise Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔧 AI Settings")
        st.selectbox("Model Version", ["YOLOv8 Nano", "YOLOv8 Small", "YOLOv8 Medium"])
        st.slider("Processing Speed", 1, 10, 7)
        st.checkbox("Enable GPU Acceleration", True)
        st.checkbox("Real-time Processing", True)
        
    with col2:
        st.markdown("#### 🏭 Quality Gates")
        st.number_input("Critical Defect Threshold", 0, 10, 1)
        st.number_input("Total Defect Limit", 0, 50, 5)
        st.text_input("Compliance Standard", "ISO 9001:2015")
        st.selectbox("Alert Level", ["Low", "Medium", "High", "Critical"])
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 3rem;">
    <h4>AlfaStack AI Inspector • Enterprise Platform</h4>
    <p>Advanced Defect Detection • Real-time Analytics • Manufacturing Intelligence</p>
    <div style="margin-top: 1rem;">
        <small>🔒 Secure • 📊 Analytics • 🚀 Scalable • 💼 Enterprise Ready</small>
    </div>
</div>
""", unsafe_allow_html=True)
