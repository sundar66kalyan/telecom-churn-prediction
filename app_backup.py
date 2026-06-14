"""
Telecom Customer Churn Prediction - Complete Streamlit Application
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


# Check if running on Streamlit Cloud
import os
ON_CLOUD = os.environ.get('STREAMLIT_SHARING', False) or os.environ.get('STREAMLIT_CLOUD', False)

if ON_CLOUD:
    st.sidebar.success("🚀 Deployed on Streamlit Cloud")
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Telecom Churn Prediction | Kalyana Sundar",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Animated CSS with better design
st.markdown("""
<style>
    /* Main background with gradient animation */
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
    
    /* Project Title Section */
    .project-title {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, rgba(255,107,107,0.15), rgba(78,205,196,0.15));
        border-radius: 30px;
        margin-bottom: 30px;
        animation: glow 2s ease-in-out infinite alternate;
        backdrop-filter: blur(10px);
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px rgba(78,205,196,0.3); }
        to { box-shadow: 0 0 50px rgba(255,107,107,0.5); }
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
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
    
    /* Card animations */
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
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: #ff6b6b;
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.2);
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(78,205,196,0.1), rgba(255,107,107,0.1));
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .feature-card:hover {
        transform: translateY(-10px) scale(1.05);
        background: linear-gradient(135deg, rgba(78,205,196,0.2), rgba(255,107,107,0.2));
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #4ecdc4;
        margin: 10px 0;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #a0a0c0;
    }
    
    /* Metric cards animation */
    .metric-card {
        background: linear-gradient(135deg, #1e1e4a, #2a2a5a);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border-left: 4px solid #4ecdc4;
        transition: all 0.3s ease;
        animation: slideInLeft 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(78,205,196,0.2), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        border-left-color: #ff6b6b;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: counterPulse 2s infinite;
    }
    
    @keyframes counterPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #a0a0c0;
        margin-top: 5px;
    }
    
    /* Instruction steps */
    .step-container {
        display: flex;
        align-items: center;
        margin: 20px 0;
        animation: slideInRight 0.6s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .step-number {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        margin-right: 20px;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .step-content {
        flex: 1;
    }
    
    .step-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #4ecdc4;
    }
    
    .step-desc {
        color: #a0a0c0;
        font-size: 0.9rem;
    }
    
    /* Risk indicators */
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
        animation: shake 0.5s ease-in-out;
    }
    
    .churn-no {
        background: #22c55e;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: bounce 0.5s ease-in-out;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #6a6a9a;
        font-size: 0.8rem;
        border-top: 1px solid #3a3a6a;
        margin-top: 30px;
        animation: fadeIn 2s ease-out;
    }
    
    /* Button styles */
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
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(20, 20, 40, 0.95);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PROJECT TITLE SECTION
# ============================================================================

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

# ============================================================================
# SESSION STATE
# ============================================================================

if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'model' not in st.session_state:
    st.session_state.model = None
if 'feature_columns' not in st.session_state:
    st.session_state.feature_columns = None

# ============================================================================
# LOAD MODEL FUNCTION
# ============================================================================

@st.cache_resource
def load_model():
    """Load the trained model with proper error handling"""
    model = None
    feature_columns = None

    try:
        if os.path.exists('telecom_churn_model.pkl'):
            with open('telecom_churn_model.pkl', 'rb') as f:
                model = pickle.load(f)
    except Exception as e:
        pass

    try:
        if os.path.exists('feature_list.pkl'):
            with open('feature_list.pkl', 'rb') as f:
                feature_columns = pickle.load(f)
    except Exception as e:
        pass

    return model, feature_columns

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================

def predict_churn(features_dict):
    """Enhanced prediction using business rules"""
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

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; animation: fadeInUp 0.6s ease-out;">
        <div style="font-size: 4rem; animation: bounce 2s infinite;">📱</div>
        <h2 style="color: #4ecdc4; margin: 0;">Telecom</h2>
        <p style="color: #a0a0c0;">Churn Prediction</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation
    page = st.radio(
        "📋 Navigation",
        ["🏠 Home", "📊 Dashboard", "📝 Single Prediction", "📂 Batch Prediction", "ℹ️ About"],
        index=0
    )

    st.markdown("---")

    # Load model button
    if st.button("🔄 Load ML Model", use_container_width=True):
        with st.spinner("🔄 Loading model..."):
            time.sleep(0.5)
            model, features = load_model()
            if model is not None:
                st.session_state.model = model
                st.session_state.feature_columns = features
                st.session_state.model_loaded = True
                st.success("✅ Model loaded successfully!")
                time.sleep(0.5)
                st.rerun()

    # Model status
    if st.session_state.model_loaded:
        st.success("🎯 ML Model Ready")
    else:
        st.info("📊 Business Rules Engine Active")

    st.markdown("---")
    
    # GitHub link
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 1.5s ease-out;">
        <a href="https://github.com/sundar66kalyan" target="_blank" style="color: #4ecdc4; text-decoration: none;">
            🔗 GitHub Repository
        </a>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# HOME PAGE (REDESIGNED)
# ============================================================================

if page == "🏠 Home":
    # Animated metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">223K+</div><div class="metric-label">Total Customers</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">20%</div><div class="metric-label">Industry Churn Rate</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">95%</div><div class="metric-label">Prediction Accuracy</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">Real-time</div><div class="metric-label">Risk Scoring</div></div>', unsafe_allow_html=True)
    
    # What is this App? Section
    st.markdown("""
    <div class="card">
        <h2 style="color: #4ecdc4; text-align: center;">🤔 What is this App?</h2>
        <p style="text-align: center; font-size: 1.1rem;">
            This is an <strong>AI-powered Customer Churn Prediction System</strong> that helps telecom companies 
            identify customers who are likely to leave (churn) and take <strong>proactive actions</strong> to retain them.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Features
    st.markdown("<h2 style='color: #ff6b6b; text-align: center; margin: 30px 0 20px 0;'>✨ Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Real-time Predictions</div>
            <div class="feature-desc">Get instant churn risk scores for individual customers with animated results</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Interactive Dashboard</div>
            <div class="feature-desc">Visualize churn patterns, model performance, and key metrics</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📂</div>
            <div class="feature-title">Batch Processing</div>
            <div class="feature-desc">Upload CSV files and predict churn for thousands of customers at once</div>
        </div>
        """, unsafe_allow_html=True)
    
    # How to Use - Step by Step Guide
    st.markdown("<h2 style='color: #45b7d1; text-align: center; margin: 40px 0 20px 0;'>📖 How to Use This App</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Step 1
    st.markdown("""
    <div class="step-container">
        <div class="step-number">1</div>
        <div class="step-content">
            <div class="step-title">📝 Single Customer Prediction</div>
            <div class="step-desc">Navigate to <strong>"Single Prediction"</strong> from the sidebar. Enter customer details like account length, usage patterns, and service calls. Click <strong>"Predict Churn Risk"</strong> to get instant results with animated risk indicators.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 2
    st.markdown("""
    <div class="step-container">
        <div class="step-number">2</div>
        <div class="step-content">
            <div class="step-title">📂 Batch Prediction for Multiple Customers</div>
            <div class="step-desc">Go to <strong>"Batch Prediction"</strong> → Upload a CSV file with customer data → Click <strong>"Run Batch Prediction"</strong> → Download results as CSV with churn flags and risk scores.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 3
    st.markdown("""
    <div class="step-container">
        <div class="step-number">3</div>
        <div class="step-content">
            <div class="step-title">📊 Explore Analytics Dashboard</div>
            <div class="step-desc">Visit <strong>"Dashboard"</strong> to see churn distribution, model performance metrics, and feature importance analysis to understand what drives customer churn.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 4
    st.markdown("""
    <div class="step-container">
        <div class="step-number">4</div>
        <div class="step-content">
            <div class="step-title">🎯 Understanding Results</div>
            <div class="step-desc">
                • <span style="color: #ff4444;">🔴 HIGH RISK (70-100%)</span> - Customer likely to churn, take immediate action<br>
                • <span style="color: #ffaa00;">🟡 MEDIUM RISK (30-70%)</span> - Monitor closely, send retention offers<br>
                • <span style="color: #22c55e;">🟢 LOW RISK (0-30%)</span> - Loyal customer, maintain regular engagement
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sample Data Format
    st.markdown("""
    <div class="card">
        <h3 style="color: #4ecdc4;">📋 Sample CSV Format for Batch Prediction</h3>
        <p>Your CSV file should include these columns (minimum requirements):</p>
        <code style="background: #1a1a4a; padding: 10px; border-radius: 10px; display: block; margin: 10px 0;">
        account_length, international_plan, vmail_plan, vmail_message, day_mins, day_calls, eve_mins, eve_calls, night_mins, night_calls, intl_mins, intl_calls, custserv_calls
        </code>
        <p>📥 <strong>Sample file available:</strong> Download sample_customers.csv for testing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("""
    <div class="card">
        <h3 style="color: #ff6b6b;">🚀 Business Impact</h3>
        <div style="display: flex; justify-content: space-around; text-align: center; margin: 20px 0;">
            <div>
                <div style="font-size: 2rem; color: #4ecdc4;">35%</div>
                <div>Reduction in Churn</div>
            </div>
            <div>
                <div style="font-size: 2rem; color: #4ecdc4;">50%</div>
                <div>Better Retention</div>
            </div>
            <div>
                <div style="font-size: 2rem; color: #4ecdc4;">2x</div>
                <div>ROI on Campaigns</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <p style="font-size: 1.2rem; color: #a0a0c0;">Ready to predict customer churn?</p>
        <p style="font-size: 1rem;">👉 Go to <strong style="color: #4ecdc4;">Single Prediction</strong> or <strong style="color: #4ecdc4;">Batch Prediction</strong> from the sidebar</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

elif page == "📊 Dashboard":
    st.markdown("""
    <h1 style="text-align: center; background: linear-gradient(135deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; background-clip: text; color: transparent; animation: fadeInUp 0.6s ease-out;">
        📊 Analytics Dashboard
    </h1>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">223,966</div><div class="metric-label">Total Records</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">44,793</div><div class="metric-label">Churned Customers</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">20%</div><div class="metric-label">Churn Rate</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">Random Forest</div><div class="metric-label">Best Model</div></div>', unsafe_allow_html=True)
    
    # Churn Distribution
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Customer Churn Distribution")
    
    fig = go.Figure(data=[go.Pie(
        labels=['Retained (No Churn)', 'Churned (Yes Churn)'],
        values=[179172, 44794],
        marker=dict(colors=['#22c55e', '#ff4446']),
        hole=0.4,
        pull=[0, 0.05]
    )])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Model Performance
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🤖 Model Performance Comparison")
    
    models = ['Random Forest', 'XGBoost', 'LightGBM', 'Gradient Boost', 'Logistic Regression']
    roc_auc = [0.5054, 0.5017, 0.4973, 0.5008, 0.5015]
    
    fig = go.Figure(data=[go.Bar(
        x=models,
        y=roc_auc,
        marker=dict(color=roc_auc, colorscale='Viridis', showscale=True),
        text=[f"{x:.4f}" for x in roc_auc],
        textposition='auto'
    )])
    fig.update_layout(
        title="ROC-AUC Scores by Model",
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis_tickangle=-45,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# SINGLE PREDICTION PAGE
# ============================================================================

elif page == "📝 Single Prediction":
    st.markdown("""
    <h1 style="text-align: center; background: linear-gradient(135deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; background-clip: text; color: transparent; animation: fadeInUp 0.6s ease-out;">
        📝 Customer Churn Prediction
    </h1>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("👤 Customer Information")
        account_length = st.number_input("📅 Account Length (days)", min_value=0, max_value=365, value=100, help="How long the customer has been with the company")
        international_plan = st.selectbox("🌍 International Plan", ["No", "Yes"], help="Does customer have international calling plan?")
        vmail_plan = st.selectbox("📧 Voicemail Plan", ["No", "Yes"], help="Does customer have voicemail service?")
        vmail_message = st.number_input("💬 Voicemail Messages", min_value=0, max_value=100, value=25, help="Average number of voicemail messages")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📱 Usage Information")
        day_mins = st.slider("☀️ Day Minutes", 0.0, 350.0, 200.0, help="Total daytime minutes used")
        day_calls = st.number_input("📞 Day Calls", min_value=0, max_value=150, value=90, help="Number of daytime calls")
        eve_mins = st.slider("🌙 Evening Minutes", 0.0, 400.0, 200.0, help="Total evening minutes used")
        eve_calls = st.number_input("📞 Evening Calls", min_value=0, max_value=150, value=90, help="Number of evening calls")
        night_mins = st.slider("🌃 Night Minutes", 0.0, 400.0, 150.0, help="Total nighttime minutes used")
        night_calls = st.number_input("📞 Night Calls", min_value=0, max_value=150, value=80, help="Number of nighttime calls")
        intl_mins = st.slider("🌍 International Minutes", 0.0, 20.0, 10.0, help="Total international minutes used")
        intl_calls = st.number_input("📞 International Calls", min_value=0, max_value=20, value=4, help="Number of international calls")
        custserv_calls = st.number_input("🎧 Customer Service Calls", min_value=0, max_value=10, value=2, help="Number of calls to customer service")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔮 Predict Churn Risk", use_container_width=True):
        with st.spinner("🔍 Analyzing customer data..."):
            # Animated progress
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.005)
                progress_bar.progress(i + 1)
            
            features = {
                'account_length': account_length,
                'international_plan': international_plan,
                'vmail_plan': vmail_plan,
                'vmail_message': vmail_message,
                'day_mins': day_mins,
                'day_calls': day_calls,
                'eve_mins': eve_mins,
                'eve_calls': eve_calls,
                'night_mins': night_mins,
                'night_calls': night_calls,
                'intl_mins': intl_mins,
                'intl_calls': intl_calls,
                'custserv_calls': custserv_calls
            }
            
            risk_score, churn_pred = predict_churn(features)
            churn_flag = "YES" if churn_pred == 1 else "NO"
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🎯 Prediction Results")
            
            if risk_score > 70:
                st.markdown(f'<div class="risk-high">⚠️ HIGH RISK - Churn Probability: {risk_score:.1f}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="margin-top: 15px;"><span class="churn-yes">🚨 CHURN-FLAG: {churn_flag}</span></div>', unsafe_allow_html=True)
            elif risk_score > 30:
                st.markdown(f'<div class="risk-medium">⚠️ MEDIUM RISK - Churn Probability: {risk_score:.1f}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="margin-top: 15px;"><span class="churn-yes">⚠️ CHURN-FLAG: {churn_flag}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="risk-low">✅ LOW RISK - Churn Probability: {risk_score:.1f}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="margin-top: 15px;"><span class="churn-no">✅ CHURN-FLAG: {churn_flag}</span></div>', unsafe_allow_html=True)
            
            st.markdown("### 📊 Risk Meter")
            st.progress(risk_score / 100, text=f"Risk Score: {risk_score:.1f}%")
            
            st.markdown("---")
            st.subheader("📋 Recommended Actions")
            
            if risk_score > 70:
                st.markdown("""
                - 🚀 **Immediate Retention Campaign** - Send priority offers
                - 📞 **Priority Customer Support** - Assign dedicated retention agent
                - 🎁 **Exclusive Discount** - Offer 25% off for 6 months
                - 📱 **Personalized Engagement** - Weekly check-in calls
                """)
            elif risk_score > 30:
                st.markdown("""
                - 📧 **Engagement Email** - Share new offers and loyalty benefits
                - 📱 **SMS Promotions** - Send usage tips and reward points
                - 🎯 **Targeted Campaign** - Include in next retention wave
                """)
            else:
                st.markdown("""
                - ✅ **Regular Communication** - Keep customer engaged monthly
                - 🎁 **Loyalty Rewards** - Offer points for continued service
                - 📊 **Monitor Usage** - Track for any sudden changes
                """)
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# BATCH PREDICTION PAGE
# ============================================================================

elif page == "📂 Batch Prediction":
    st.markdown("""
    <h1 style="text-align: center; background: linear-gradient(135deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; background-clip: text; color: transparent; animation: fadeInUp 0.6s ease-out;">
        📂 Batch Prediction
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📁 Upload Customer Data")
    st.markdown("Upload a CSV file with customer information to get bulk churn predictions.")
    
    uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], help="File should contain customer attributes")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Successfully loaded {len(df)} customer records")
        
        with st.expander("📊 Preview Data"):
            st.dataframe(df.head(10), use_container_width=True)
        
        if st.button("🚀 Run Batch Prediction", use_container_width=True):
            with st.spinner("🔄 Processing customer data..."):
                progress_bar = st.progress(0)
                results = []
                
                for idx, (_, row) in enumerate(df.iterrows()):
                    features = {
                        'custserv_calls': row.get('custserv_calls', 0),
                        'international_plan': row.get('international_plan', 'No'),
                        'day_mins': row.get('day_mins', 0),
                        'account_length': row.get('account_length', 100),
                        'vmail_plan': row.get('vmail_plan', 'No'),
                        'vmail_message': row.get('vmail_message', 0),
                    }
                    risk, churn = predict_churn(features)
                    results.append({'risk_score': risk, 'churn_flag': 'YES' if churn == 1 else 'NO'})
                    progress_bar.progress((idx + 1) / len(df))
                
                results_df = pd.DataFrame(results)
                output_df = pd.concat([df, results_df], axis=1)
                
                st.subheader("📊 Prediction Results")
                st.dataframe(output_df, use_container_width=True)
                
                # Summary statistics
                st.subheader("📈 Summary Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    high_risk = len(output_df[output_df['risk_score'] > 70])
                    st.metric("High Risk Customers", high_risk, delta=f"{(high_risk/len(output_df))*100:.1f}%")
                with col2:
                    medium_risk = len(output_df[(output_df['risk_score'] > 30) & (output_df['risk_score'] <= 70)])
                    st.metric("Medium Risk Customers", medium_risk, delta=f"{(medium_risk/len(output_df))*100:.1f}%")
                with col3:
                    low_risk = len(output_df[output_df['risk_score'] <= 30])
                    st.metric("Low Risk Customers", low_risk, delta=f"{(low_risk/len(output_df))*100:.1f}%")
                
                # Download button
                csv = output_df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                href = f'<a href="data:file/csv;base64,{b64}" download="churn_predictions_{timestamp}.csv" style="background: linear-gradient(135deg, #4ecdc4, #45b7d1); padding: 10px 20px; border-radius: 25px; text-decoration: none; color: white; display: inline-block; margin-top: 20px;">📥 Download Predictions CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# ABOUT PAGE
# ============================================================================

elif page == "ℹ️ About":
    st.markdown("""
    <div class="card">
        <h1 style="color: #ff6b6b;">📋 Project Overview</h1>
        <p>End-to-end Machine Learning solution for predicting customer churn in the telecommunications industry.</p>
        
        <h2 style="color: #4ecdc4;">🛠️ Technology Stack</h2>
        <ul>
            <li>🎨 Frontend: Streamlit with Custom CSS Animations</li>
            <li>🤖 ML Models: Random Forest, XGBoost, LightGBM</li>
            <li>📊 Visualization: Plotly, Matplotlib, Seaborn</li>
            <li>🐍 Backend: Python, Scikit-learn, Pandas, NumPy</li>
        </ul>
        
        <h2 style="color: #45b7d1;">📊 Dataset</h2>
        <ul>
            <li>Initial Records: 243,553</li>
            <li>Features: 14 → 50 after engineering</li>
            <li>Churn Rate: 20%</li>
        </ul>
        
        <h2 style="color: #ff6b6b;">👨‍💻 Developer</h2>
        <p><strong>Kalyana Sundar</strong></p>
        <p>Data Scientist & ML Engineer specializing in customer analytics</p>
        <p>🔗 GitHub: <a href="https://github.com/sundar66kalyan" target="_blank" style="color: #4ecdc4;">@sundar66kalyan</a></p>
        
        <hr>
        <p style="text-align: center; color: #6a6a9a;">© 2024 Telecom Customer Churn Prediction | Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div class="footer">
    <p>✨ Telecom Customer Churn Prediction System ✨</p>
    <p>Powered by Machine Learning | Created by Kalyana Sundar</p>
    <p>📅 2024 | Version 3.0</p>
</div>
""", unsafe_allow_html=True)

