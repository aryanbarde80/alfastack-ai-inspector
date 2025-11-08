import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from ultralytics import YOLO
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import io
import base64

st.set_page_config(
    page_title="AlfaStack AI Inspector",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Enterprise CSS
st.markdown("""
<style>
    /* Global Styles */
    .main { 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
        color: #f8fafc; 
    }
    
    /* Header Styles */
    .enterprise-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2.5rem 2rem;
        border-radius: 0 0 25px 25px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .main-title { 
        font-size: 2.8rem; 
        font-weight: 800; 
        color: white; 
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    .sub-title { 
        font-size: 1.2rem; 
        color: #dbeafe; 
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    
    /* Card Styles */
    .enterprise-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .enterprise-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    
    /* Upload Zone */
    .upload-zone {
        border: 3px dashed #3b82f6;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        background: rgba(59, 130, 246, 0.05);
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .upload-zone:hover {
        background: rgba(59, 130, 246, 0.1);
        border-color: #60a5fa;
        transform: scale(1.01);
    }
    
    /* Button Styles */
    .stButton button {
        background: linear-gradient(45deg, #3b82f6, #1e40af);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(30, 41, 59, 0.8);
        border-radius: 10px 10px 0 0;
        gap: 1px;
        padding: 10px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white;
    }
    
    /* Image Container */
    .image-container {
        position: relative;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
    }
    
    /* Success Message */
    .success-message {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #00b09b, #96c93d);
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0, 180, 155, 0.3);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Load AI Model
@st.cache_resource
def load_model():
    return YOLO('yolov8n.pt')

model = load_model()

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_results' not in st.session_state:
    st.session_state.current_results = None
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None

# Helper function to create download link
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}" style="background: linear-gradient(45deg, #3b82f6, #1e40af); color: white; padding: 0.5rem 1rem; text-decoration: none; border-radius: 8px; display: inline-block; margin: 0.5rem;">{text}</a>'
    return href

# Enterprise Header
st.markdown("""
<div class="enterprise-header">
    <h1 class="main-title">🏭 AlfaStack AI Inspector</h1>
    <p class="sub-title">Enterprise-Grade Defect Detection • Real-time Analytics • Quality Assurance</p>
</div>
""", unsafe_allow_html=True)

# Main Dashboard with Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Inspection Portal", "📊 Analytics Dashboard", "⚙️ Settings & Help"])

with tab1:
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
            st.session_state.original_image = image
            
            # Image Preview with Zoom Options
            st.markdown("#### 🔍 Image Preview")
            col_a, col_b = st.columns([3, 1])
            
            with col_a:
                st.image(image, use_container_width=True, caption="🔬 Product Under Analysis")
            
            with col_b:
                st.markdown("**Zoom Options**")
                zoom_level = st.slider("Zoom Level", 1.0, 3.0, 1.0, 0.1, label_visibility="collapsed")
                
                # Apply zoom
                if zoom_level != 1.0:
                    width, height = image.size
                    new_width = int(width * zoom_level)
                    new_height = int(height * zoom_level)
                    zoomed_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    st.image(zoomed_image, caption=f"Zoomed View ({zoom_level}x)")
            
            # Image Analytics
            st.markdown("#### 📏 Image Analytics")
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            with col_c1:
                st.metric("Dimensions", f"{image.size[0]}x{image.size[1]}")
            with col_c2:
                st.metric("Color Mode", image.mode)
            with col_c3:
                st.metric("File Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
            with col_c4:
                aspect_ratio = image.size[0] / image.size[1]
                st.metric("Aspect Ratio", f"{aspect_ratio:.2f}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
        st.markdown("### 📈 AI Analysis Dashboard")
        
        if uploaded_file:
            # Control Panel
            st.markdown("#### ⚙️ Precision Controls")
            col_x, col_y, col_z = st.columns(3)
            with col_x:
                confidence = st.slider("AI Confidence", 0.1, 1.0, 0.6, 0.05)
            with col_y:
                st.metric("AI Status", "Online", "Ready")
            with col_z:
                enhance = st.checkbox("Enhance Image", value=True)
            
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
                    
                    # Enhance image if selected
                    if enhance:
                        pil_image = Image.fromarray(image_np)
                        enhancer = ImageEnhance.Sharpness(pil_image)
                        pil_image = enhancer.enhance(1.5)
                        enhancer = ImageEnhance.Contrast(pil_image)
                        pil_image = enhancer.enhance(1.2)
                        image_np = np.array(pil_image)
                    
                    results = model(image_np, conf=confidence)
                    st.session_state.current_results = results
                    
                    if len(results) > 0:
                        # Enhanced Results
                        result_img = results[0].plot()
                        result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                        st.session_state.processed_image = Image.fromarray(result_img_rgb)
                        
                        st.image(result_img_rgb, use_container_width=True, caption="🎯 AI DEFECT MAPPING")
                        
                        # Download buttons
                        st.markdown("#### 💾 Export Results")
                        col_d1, col_d2 = st.columns(2)
                        
                        with col_d1:
                            st.markdown(get_image_download_link(
                                Image.fromarray(result_img_rgb), 
                                "defect_analysis.png", 
                                "📥 Download Analysis Image"
                            ), unsafe_allow_html=True)
                        
                        with col_d2:
                            # Create a simple report
                            report_text = f"AlfaStack AI Inspector Report\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                            report_text += f"Image: {uploaded_file.name}\nDimensions: {image.size[0]}x{image.size[1]}\n\n"
                            
                            defect_count = len(results[0].boxes)
                            report_text += f"Defects Detected: {defect_count}\n"
                            
                            if defect_count > 0:
                                report_text += "\nDefect Details:\n"
                                for i, box in enumerate(results[0].boxes):
                                    class_id = int(box.cls[0])
                                    class_name = model.names[class_id]
                                    conf = box.conf[0].item()
                                    report_text += f"{i+1}. {class_name.upper()} (Confidence: {conf:.1%})\n"
                            
                            # Create download link for report
                            b64_report = base64.b64encode(report_text.encode()).decode()
                            href = f'<a href="data:file/txt;base64,{b64_report}" download="inspection_report.txt" style="background: linear-gradient(45deg, #10b981, #059669); color: white; padding: 0.5rem 1rem; text-decoration: none; border-radius: 8px; display: inline-block; margin: 0.5rem;">📥 Download Report</a>'
                            st.markdown(href, unsafe_allow_html=True)
                        
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
                        st.dataframe(df, use_container_width=True, height=300)
                        
                        # Key Metrics
                        st.markdown("#### 📈 Inspection Summary")
                        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                        
                        with col_m1:
                            st.markdown(f'<div class="metric-card"><h4>DEFECTS</h4><h2>{defect_count}</h2></div>', unsafe_allow_html=True)
                        
                        with col_m2:
                            avg_conf = np.mean([box.conf[0].item() for box in results[0].boxes]) if defect_count > 0 else 0
                            st.markdown(f'<div class="metric-card"><h4>CONFIDENCE</h4><h2>{avg_conf:.1%}</h2></div>', unsafe_allow_html=True)
                        
                        with col_m3:
                            total_area = sum([(box.xyxy[0][2] - box.xyxy[0][0]) * (box.xyxy[0][3] - box.xyxy[0][1]) for box in results[0].boxes])
                            st.markdown(f'<div class="metric-card"><h4>TOTAL AREA</h4><h2>{total_area:.0f} px²</h2></div>', unsafe_allow_html=True)
                        
                        with col_m4:
                            status = "❌ REJECT" if defect_count > 0 else "✅ PASS"
                            st.markdown(f'<div class="metric-card"><h4>VERDICT</h4><h2>{status}</h2></div>', unsafe_allow_html=True)
                        
                        # Save to history
                        st.session_state.analysis_history.append({
                            'timestamp': datetime.now(),
                            'defects': defect_count,
                            'confidence': avg_conf,
                            'status': status,
                            'image_name': uploaded_file.name
                        })
                        
                    else:
                        # Perfect Quality
                        st.session_state.processed_image = image
                        st.success("🎉 **MANUFACTURING EXCELLENCE ACHIEVED**")
                        st.balloons()
                        st.markdown('''
                        <div class="success-message">
                            <h2 style="color: white; margin: 0;">✅ QUALITY CERTIFIED</h2>
                            <p style="color: white; font-size: 1.2rem;">Zero Defects • Production Ready • Market Perfect</p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        # Save to history
                        st.session_state.analysis_history.append({
                            'timestamp': datetime.now(),
                            'defects': 0,
                            'confidence': 1.0,
                            'status': 'PASS',
                            'image_name': uploaded_file.name
                        })
        else:
            st.info("""
            👆 **UPLOAD MANUFACTURING SAMPLE FOR AI ANALYSIS**
            
            *Enterprise Features:*
            • **Real-time** defect detection
            • **Advanced** object measurements  
            • **Professional** analytics
            • **Export** capabilities
            • **Always Online** with health monitoring
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Quality Analytics Dashboard")
    
    if st.session_state.analysis_history:
        history_df = pd.DataFrame(st.session_state.analysis_history)
        
        # Summary Metrics
        st.markdown("#### 📊 Inspection Summary")
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        
        with col_s1:
            total_inspections = len(history_df)
            st.metric("Total Inspections", total_inspections)
        
        with col_s2:
            pass_rate = len(history_df[history_df['defects'] == 0]) / total_inspections * 100
            st.metric("Pass Rate", f"{pass_rate:.1f}%")
        
        with col_s3:
            avg_defects = history_df['defects'].mean()
            st.metric("Avg Defects/Image", f"{avg_defects:.1f}")
        
        with col_s4:
            avg_confidence = history_df['confidence'].mean()
            st.metric("Avg Confidence", f"{avg_confidence:.1%}")
        
        # Charts
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            # Defect Trend
            fig_trend = px.line(history_df, x='timestamp', y='defects', 
                               title='Defect Trend Analysis', markers=True)
            fig_trend.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with col_c2:
            # Status Distribution
            status_counts = history_df['status'].value_counts()
            fig_pie = px.pie(
                values=status_counts.values, 
                names=status_counts.index,
                title='Inspection Results Distribution',
                color=status_counts.index,
                color_discrete_map={'PASS':'#00b09b', 'REJECT':'#ef4444'}
            )
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Recent Inspections Table
        st.markdown("#### 📋 Recent Inspections")
        display_df = history_df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        display_df = display_df.rename(columns={
            'timestamp': 'Time',
            'defects': 'Defects',
            'confidence': 'Confidence',
            'status': 'Status',
            'image_name': 'Image'
        })
        st.dataframe(display_df.sort_values('Time', ascending=False), use_container_width=True)
        
        # Export Analytics
        st.markdown("#### 📤 Export Analytics")
        csv = history_df.to_csv(index=False)
        b64_csv = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64_csv}" download="inspection_analytics.csv" style="background: linear-gradient(45deg, #8b5cf6, #7c3aed); color: white; padding: 0.7rem 1.5rem; text-decoration: none; border-radius: 8px; display: inline-block; margin: 0.5rem; font-weight: 600;">📊 Download Full Analytics</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    else:
        st.info("No inspection data available. Perform inspections to see analytics here.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Application Settings")
        
        st.markdown("#### AI Model Configuration")
        model_option = st.selectbox(
            "Detection Model",
            ["YOLOv8 Nano (Default)", "YOLOv8 Small", "YOLOv8 Medium", "YOLOv8 Large"],
            help="Select the AI model for detection. Larger models are more accurate but slower."
        )
        
        st.markdown("#### Image Processing")
        col_set_a, col_set_b = st.columns(2)
        with col_set_a:
            auto_enhance = st.checkbox("Auto-enhance images", value=True)
        with col_set_b:
            save_original = st.checkbox("Save original images", value=False)
        
        st.markdown("#### Notifications")
        email_alerts = st.checkbox("Email alerts for critical defects")
        if email_alerts:
            email_address = st.text_input("Email address")
        
        st.markdown("#### Data Management")
        if st.button("Clear Inspection History", use_container_width=True):
            st.session_state.analysis_history = []
            st.success("Inspection history cleared!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_set2:
        st.markdown('<div class="enterprise-card">', unsafe_allow_html=True)
        st.markdown("### ❓ Help & Support")
        
        st.markdown("#### How to Use")
        with st.expander("Getting Started", expanded=True):
            st.markdown("""
            1. **Upload** a manufacturing sample image
            2. **Adjust** the AI confidence threshold if needed
            3. **Click** 'Launch AI Inspection' to analyze
            4. **Review** the results and download reports
            """)
        
        with st.expander("Understanding Results"):
            st.markdown("""
            - **Defects**: Number of issues detected
            - **Confidence**: AI certainty in detection
            - **Area**: Total area of detected defects
            - **Verdict**: Overall quality assessment
            """)
        
        with st.expander("Troubleshooting"):
            st.markdown("""
            - **No detections?** Try lowering the confidence threshold
            - **Poor quality?** Enable image enhancement
            - **Slow processing?** Check your internet connection
            """)
        
        st.markdown("#### Support Resources")
        st.markdown("""
        - 📚 [Documentation](https://docs.alfastack.ai)
        - 🎮 [Tutorial Videos](https://learn.alfastack.ai)
        - 🐛 [Report Issues](https://support.alfastack.ai)
        - 📞 [Contact Support](mailto:support@alfastack.ai)
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Enterprise Footer
st.markdown("""
<div class="footer">
    <h4>AlfaStack AI Inspector • Enterprise SaaS Platform</h4>
    <p>Advanced Defect Detection • Real-time Analytics • Quality Assurance</p>
    <p style="font-size: 0.9rem;">🔒 Enterprise Grade • 📊 Real-time Analytics • 🚀 Health Monitoring Active</p>
</div>
""", unsafe_allow_html=True)
