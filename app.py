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
    st.error("Error: Model file not found. Please ensure 'model.pkl' is in the folder.")
    st.stop()

# Input Section
st.header("Enter Student Details")

# Layout with two columns for better look
col1, col2 = st.columns(2)

with col1:
    study = st.slider("Study Hours", 0, 15, 5)
    sleep = st.slider("Sleep Hours", 0, 15, 7)
    social = st.slider("Social Media Usage", 0, 10, 2)
    pressure = st.slider("Academic Pressure (1-5)", 1, 5, 3)
    family = st.slider("Family Support (1-5)", 1, 5, 4)

with col2:
    activity = st.slider("Physical Activity", 0, 10, 1)
    screen = st.slider("Total Screen Time", 0, 15, 4)
    extra = st.slider("Extracurricular Activities", 0, 10, 1)
    financial = st.slider("Financial Stress (1-5)", 1, 5, 2)
    examfear = st.slider("Exam Anxiety (1-5)", 1, 5, 2)
    timemanagement = st.slider("Time Management (1-5)", 1, 5, 3)

# Logic for "Correct Data" Check
total_hours = study + sleep + social + activity + extra
remaining_hours = 24 - total_hours

# Button
if st.button("Predict Stress"):
    # 1. Check if data is realistic
    if total_hours > 24:
        st.warning(f"⚠️ **Data Alert:** You have logged {total_hours} hours of activity. A day only has 24 hours. Please adjust your sliders for an accurate prediction.")
    else:
        # 2. Prepare data for model
        data_input = np.array([[study, sleep, social, pressure, family,
                                activity, screen, extra, financial,
                                examfear, timemanagement]])

        # 3. Prediction
        prediction = model.predict(data_input)

        st.subheader("Results")
        if prediction[0] == 1:
            st.error("Model Prediction: High Risk of Stress")
        else:
            st.success("Model Prediction: Low Risk of Stress")

        # 4. Professional Suggestions (Simple English)
        st.subheader("Personalized Suggestions")

        if sleep < 6:
            st.write("• Maintain a proper sleep schedule.")
        if study > 7:
            st.write("• Take regular breaks during study time.")
        if social > 5:
            st.write("• Limit your social media usage.")
        if pressure > 3:
            st.write("• Manage academic tasks step by step.")
        if family < 3:
            st.write("• Seek support from family or close ones.")
        if activity < 2:
            st.write("• Include physical activity in your routine.")
        if screen > 7:
            st.write("• Reduce screen time and take breaks.")
        if financial > 3:
            st.write("• Discuss financial concerns with a trusted person.")
        if examfear > 3:
            st.write("• Practice regularly to build confidence.")
        if timemanagement < 3:
            st.write("• Follow a structured daily schedule.")