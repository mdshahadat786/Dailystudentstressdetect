import streamlit as st
import pickle
import numpy as np

# Title
st.title("AI Student Stress Detection System")

# Load model
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    st.success("Model Loaded ✅")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Input Section
st.header("Enter Student Details")

study = st.slider("Study Hours", 0, 10)
sleep = st.slider("Sleep Hours", 0, 10)
social = st.slider("Social Media Usage", 0, 8)
pressure = st.slider("Academic Pressure", 1, 5)
family = st.slider("Family Support", 1, 5)
activity = st.slider("Physical Activity", 0, 5)
screen = st.slider("Screen Time", 0, 10)
extra = st.slider("Extracurricular Activities", 0, 5)
financial = st.slider("Financial Stress", 1, 5)
examfear = st.slider("Exam Fear", 1, 5)
timemanagement = st.slider("Time Management", 1, 5)

# Button
if st.button("Predict Stress"):
    # Prepare data for model
    data_input = np.array([[study, sleep, social, pressure, family,
                            activity, screen, extra, financial,
                            examfear, timemanagement]])

    # Prediction
    prediction = model.predict(data_input)

    # Manual Stress Score Calculation
    stress_score = 0
    if sleep < 6: stress_score += 20
    if study > 7: stress_score += 15
    if social > 5: stress_score += 10
    if pressure > 3: stress_score += 20
    if family < 3: stress_score += 10
    if activity < 2: stress_score += 10
    if screen > 7: stress_score += 10
    if financial > 3: stress_score += 10
    if examfear > 3: stress_score += 10
    if timemanagement < 3: stress_score += 10

    st.subheader("Results")
    st.write(f"Calculated Stress Score: {stress_score}")

    if prediction[0] == 1:
        st.error("Model Prediction: High Risk of Stress")
    else:
        st.success("Model Prediction: Low Risk of Stress")

    # Professional Suggestions (Simple English)
    st.subheader("Personalized Suggestions")

    if sleep < 6:
        st.write("Maintain a proper sleep schedule.")
    if study > 7:
        st.write("Take regular breaks during study time.")
    if social > 5:
        st.write("Limit your social media usage.")
    if pressure > 3:
        st.write("Manage academic tasks step by step.")
    if family < 3:
        st.write("Seek support from family or close ones.")
    if activity < 2:
        st.write("Include physical activity in your routine.")
    if screen > 7:
        st.write("Reduce screen time and take breaks.")
    if financial > 3:
        st.write("Discuss financial concerns with a trusted person.")
    if examfear > 3:
        st.write("Practice regularly to build confidence.")
    if timemanagement < 3:
        st.write("Follow a structured daily schedule.")