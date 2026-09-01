import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Student Analytics Portal", page_icon="🎓", layout="wide")

# --- SESSION STATE FOR NAVIGATION ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# --- TOP NAVIGATION BUTTONS ---
st.title("🎓 Student Performance Analytics Portal")

nav_col1, nav_col2, nav_col3, _ = st.columns([1, 1, 1, 2])

with nav_col1:
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.current_page == "Home" else "secondary"):
        st.session_state.current_page = "Home"
        st.rerun()

with nav_col2:
    if st.button("🔮 Prediction", use_container_width=True, type="primary" if st.session_state.current_page == "Prediction" else "secondary"):
        st.session_state.current_page = "Prediction"
        st.rerun()

with nav_col3:
    if st.button("📊 Insights", use_container_width=True, type="primary" if st.session_state.current_page == "Insights" else "secondary"):
        st.session_state.current_page = "Insights"
        st.rerun()

st.divider()

# ==========================================
# PAGE 1: HOME
# ==========================================
if st.session_state.current_page == "Home":
    st.header("📌 Overview")
    st.markdown("Welcome to the Student Analytics Portal. This system predicts student performance using machine learning.")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Model Status", "Active")
    m2.metric("Input Metrics", "4 Parameters")
    m3.metric("Backend API", "FastAPI Connected")

    st.subheader("💡 Features")
    st.markdown("""
    * **Instant Inference:** Real-time ML predictions via REST API.
    * **Multi-Class Outputs:** Classifies into *Excellent*, *Good*, *Average*, and *Poor*.
    * **Scalable Architecture:** Fully decoupled FastAPI backend and Streamlit frontend.
    """)

# ==========================================
# PAGE 2: PREDICTION
# ==========================================
elif st.session_state.current_page == "Prediction":
    st.header("🔮 Make Performance Prediction")
    
    st.sidebar.subheader("📊 Input Metrics")
    study_hours = st.sidebar.slider("Study Hours (per week)", 0, 100, 45)
    attendance = st.sidebar.slider("Attendance (%)", 0, 100, 80)
    assignments = st.sidebar.slider("Assignment Score (%)", 0, 100, 75)
    exam_score = st.sidebar.slider("Exam Score (%)", 0, 100, 65)

    payload = {
        "study_hours": study_hours,
        "attendance": attendance,
        "assignments": assignments,
        "exam_score": exam_score
    }

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📋 Input Summary")
        st.json(payload)
        predict_btn = st.button("🚀 Predict Result", type="primary", use_container_width=True)

    with col2:
        st.subheader("🎯 Result")
        if predict_btn:
            try:
                res = requests.post(BACKEND_URL, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"### Predicted Category: **{data['prediction_label']}**")
                    
                    if "probabilities" in data:
                        st.subheader("📊 Class Probabilities")
                        st.bar_chart(data["probabilities"])
                else:
                    st.error("Backend Error: " + res.text)
            except Exception as e:
                st.error(f"Cannot connect to Backend API: {e}")
        else:
            st.info("Set parameters in sidebar and click **Predict Result**.")

# ==========================================
# PAGE 3: INSIGHTS
# ==========================================
elif st.session_state.current_page == "Insights":
    st.header("📊 Model Insights & Feature Importance")
    
    df_features = pd.DataFrame({
        "Feature": ["Exam Score", "Attendance", "Study Hours", "Assignments"],
        "Impact Level": ["High", "High", "Medium", "Medium"]
    })
    st.table(df_features)