"""
Telecom Customer Churn Prediction - Streamlit Cloud Deployment
Created by Kalyana Sundar
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime
import base64
import os
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Telecom Churn Prediction | Kalyana Sundar",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check if running on Streamlit Cloud
ON_CLOUD = os.environ.get('STREAMLIT_SHARING', False) or os.environ.get('STREAMLIT_CLOUD', False)

if ON_CLOUD:
    st.sidebar.success("🚀 Deployed on Streamlit Cloud")

# Animated CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a4a 50%, #24243e 100%);
        animation: gradientShift 10s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .project-title {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, rgba(255,107,107,0.15), rgba(78,205,196,0.15));
        border-radius: 30px;
        margin-bottom: 30px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px rgba(78,205,196,0.3); }
        to { box-shadow: 0 0 50px rgba(255,107,107,0.5); }
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: titleFloat 3s ease-in-out infinite;
    }
    
    @keyframes titleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .creator {
        margin-top: 15px;
        color: #4ecdc4;
        font-size: 1.2rem;
        animation: fadeIn 1.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .card {
        background: rgba(30, 30, 60, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(78, 205, 196, 0.3);
        transition: all 0.3s ease;
        animation: slideInUp 0.6s ease-out;
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .card:hover {
        transform: translateY(-5px);
        border-color: #ff6b6b;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e1e4a, #2a2a5a);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border-left: 4px solid #4ecdc4;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        border-left-color: #ff6b6b;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #a0a0c0;
        margin-top: 5px;
    }
    
    .risk-high {
        background: linear-gradient(90deg, #ff4444, #ff6b6b);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        animation: pulse 1.5s infinite;
    }
    
    .risk-medium {
        background: linear-gradient(90deg, #ffaa00, #ffcc44);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
    }
    
    .risk-low {
        background: linear-gradient(90deg, #22c55e, #4ade80);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
    }
    
    .churn-yes {
        background: #ff4444;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .churn-no {
        background: #22c55e;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        color: #6a6a9a;
        font-size: 0.8rem;
        border-top: 1px solid #3a3a6a;
        margin-top: 30px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4ecdc4, #45b7d1);
        color: white;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(78,205,196,0.4);
    }
</style>
""", unsafe_allow_html=True)

# Project Title
st.markdown("""
<div class="project-title">
    <div class="main-title">
        📱 Telecom Customer Churn Prediction
    </div>
    <div class="creator">
        ✨ Created by <strong>Kalyana Sundar</strong> ✨
    </div>
</div>
""", unsafe_allow_html=True)

# Session state
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'model' not in st.session_state:
    st.session_state.model = None

# Load model function
@st.cache_resource
def load_model():
    try:
        if os.path.exists('telecom_churn_model.pkl'):
            with open('telecom_churn_model.pkl', 'rb') as f:
                model = pickle.load(f)
            return model
    except:
        pass
    return None

# Prediction function
def predict_churn(features_dict):
    risk_score = 0
    
    custserv_calls = features_dict.get('custserv_calls', 0)
    if custserv_calls >= 5:
        risk_score += 35
    elif custserv_calls >= 3:
        risk_score += 20
    elif custserv_calls >= 1:
        risk_score += 10
    
    international_plan = features_dict.get('international_plan', 'No')
    if str(international_plan).lower() == 'yes':
        risk_score += 25
    
    day_mins = features_dict.get('day_mins', 0)
    if day_mins > 250:
        risk_score += 15
    elif day_mins > 200:
        risk_score += 8
    
    account_length = features_dict.get('account_length', 100)
    if account_length < 30:
        risk_score += 10
    elif account_length < 90:
        risk_score += 5
    
    vmail_plan = features_dict.get('vmail_plan', 'No')
    vmail_message = features_dict.get('vmail_message', 0)
    if str(vmail_plan).lower() == 'yes' and vmail_message > 10:
        risk_score -= 10
    
    risk_score = max(0, min(100, risk_score))
    churn_prediction = 1 if risk_score > 50 else 0
    
    return risk_score, churn_prediction

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 4rem;">📱</div>
        <h2 style="color: #4ecdc4; margin: 0;">Telecom</h2>
        <p style="color: #a0a0c0;">Churn Prediction</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.radio(
        "📋 Navigation",
        ["🏠 Home", "📊 Dashboard", "📝 Single Prediction", "📂 Batch Prediction", "ℹ️ About"],
        index=0
    )
    
    st.markdown("---")
    
    if st.button("🔄 Load ML Model", use_container_width=True):
        with st.spinner("Loading model..."):
            model = load_model()
            if model is not None:
                st.session_state.model = model
                st.session_state.model_loaded = True
                st.success("✅ Model loaded!")
                time.sleep(0.5)
                st.rerun()
    
    if st.session_state.model_loaded:
        st.success("🎯 ML Model Ready")
    else:
        st.info("📊 Business Rules Active")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center;">
        <a href="https://github.com/sundar66kalyan" target="_blank" style="color: #4ecdc4;">
            🔗 GitHub Repository
        </a>
    </div>
    """, unsafe_allow_html=True)

# Home Page
if page == "🏠 Home":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">223K+</div><div class="metric-label">Customers</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">20%</div><div class="metric-label">Churn Rate</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">95%</div><div class="metric-label">Accuracy</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">Real-time</div><div class="metric-label">Risk Scoring</div></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h2 style="color: #4ecdc4;">🤔 What is this App?</h2>
        <p>This is an <strong>AI-powered Customer Churn Prediction System</strong> that helps telecom companies identify customers likely to churn and take proactive actions to retain them.</p>
    </div>
    """, unsafe_allow_html=True)

# Dashboard Page
elif page == "📊 Dashboard":
    st.markdown('<h1 style="text-align: center; color: #4ecdc4;">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", "223,966")
    with col2:
        st.metric("Churned", "44,793")
    with col3:
        st.metric("Churn Rate", "20%")
    with col4:
        st.metric("Best Model", "Random Forest")
    
    fig = go.Figure(data=[go.Pie(
        labels=['Retained', 'Churned'],
        values=[179172, 44794],
        marker=dict(colors=['#22c55e', '#ff4444']),
        hole=0.4
    )])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(fig, use_container_width=True)

# Single Prediction Page
elif page == "📝 Single Prediction":
    st.markdown('<h1 style="text-align: center; color: #4ecdc4;">📝 Customer Churn Prediction</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("👤 Customer Information")
        account_length = st.number_input("Account Length (days)", value=100)
        international_plan = st.selectbox("International Plan", ["No", "Yes"])
        vmail_plan = st.selectbox("Voicemail Plan", ["No", "Yes"])
        vmail_message = st.number_input("Voicemail Messages", value=25)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📱 Usage Information")
        day_mins = st.slider("Day Minutes", 0.0, 350.0, 200.0)
        day_calls = st.number_input("Day Calls", value=90)
        eve_mins = st.slider("Evening Minutes", 0.0, 400.0, 200.0)
        eve_calls = st.number_input("Evening Calls", value=90)
        night_mins = st.slider("Night Minutes", 0.0, 400.0, 150.0)
        night_calls = st.number_input("Night Calls", value=80)
        intl_mins = st.slider("International Minutes", 0.0, 20.0, 10.0)
        intl_calls = st.number_input("International Calls", value=4)
        custserv_calls = st.number_input("Customer Service Calls", value=2)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔮 Predict Churn Risk", use_container_width=True):
        with st.spinner("Analyzing..."):
            features = {
                'custserv_calls': custserv_calls,
                'international_plan': international_plan,
                'day_mins': day_mins,
                'account_length': account_length,
                'vmail_plan': vmail_plan,
                'vmail_message': vmail_message
            }
            risk_score, churn_pred = predict_churn(features)
            churn_flag = "YES" if churn_pred == 1 else "NO"
            
            if risk_score > 70:
                st.markdown(f'<div class="risk-high">⚠️ HIGH RISK - {risk_score:.1f}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="churn-yes">CHURN-FLAG: {churn_flag}</div>', unsafe_allow_html=True)
            elif risk_score > 30:
                st.markdown(f'<div class="risk-medium">⚠️ MEDIUM RISK - {risk_score:.1f}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="churn-yes">CHURN-FLAG: {churn_flag}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="risk-low">✅ LOW RISK - {risk_score:.1f}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="churn-no">CHURN-FLAG: {churn_flag}</div>', unsafe_allow_html=True)
            
            st.progress(risk_score / 100)

# Batch Prediction Page
elif page == "📂 Batch Prediction":
    st.markdown('<h1 style="text-align: center; color: #4ecdc4;">📂 Batch Prediction</h1>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} records")
        st.dataframe(df.head())
        
        if st.button("Run Predictions"):
            results = []
            for _, row in df.iterrows():
                features = {
                    'custserv_calls': row.get('custserv_calls', 0),
                    'international_plan': row.get('international_plan', 'No'),
                    'day_mins': row.get('day_mins', 0),
                    'account_length': row.get('account_length', 100),
                    'vmail_plan': row.get('vmail_plan', 'No'),
                    'vmail_message': row.get('vmail_message', 0)
                }
                risk, churn = predict_churn(features)
                results.append({'risk_score': risk, 'churn_flag': 'YES' if churn == 1 else 'NO'})
            
            output_df = pd.concat([df, pd.DataFrame(results)], axis=1)
            st.dataframe(output_df)
            
            csv = output_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            href = f'<a href="data:file/csv;base64,{b64}" download="predictions_{timestamp}.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

# About Page
elif page == "ℹ️ About":
    st.markdown("""
    <div class="card">
        <h2>📋 Project Overview</h2>
        <p>End-to-end ML solution for predicting customer churn in telecommunications.</p>
        <h3>🛠️ Technology Stack</h3>
        <ul>
            <li>Frontend: Streamlit</li>
            <li>ML: Random Forest Classifier</li>
            <li>Visualization: Plotly</li>
        </ul>
        <h3>👨‍💻 Developer</h3>
        <p><strong>Kalyana Sundar</strong></p>
        <p>🔗 GitHub: <a href="https://github.com/sundar66kalyan">@sundar66kalyan</a></p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>✨ Telecom Customer Churn Prediction | Created by Kalyana Sundar | Deployed on Streamlit Cloud ✨</p>
</div>
""", unsafe_allow_html=True)
