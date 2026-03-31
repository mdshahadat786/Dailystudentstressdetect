import streamlit as st
import pickle
import numpy as np

# Page configuration
st.set_page_config(page_title="Stress Detection", layout="centered")

# Title
st.title("Student Stress Detection System")

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

# All inputs in one single vertical list
study = st.slider("Study Hours", 0, 15, 5)
sleep = st.slider("Sleep Hours", 0, 15, 7)
social = st.slider("Social Media Usage", 0, 10, 2)
pressure = st.slider("Academic Pressure (1-5)", 1, 5, 3)
family = st.slider("Family Support (1-5)", 1, 5, 4)
activity = st.slider("Physical Activity", 0, 10, 1)
screen = st.slider("Total Screen Time", 0, 15, 4)
extra = st.slider("Extracurricular Activities", 0, 10, 1)
financial = st.slider("Financial Stress (1-5)", 1, 5, 2)
examfear = st.slider("Exam Anxiety (1-5)", 1, 5, 2)
timemanagement = st.slider("Time Management (1-5)", 1, 5, 3)

# Logic for "Correct Data" Check
total_hours = study + sleep + social + activity + extra

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

        # 3. Model Prediction
        prediction = model.predict(data_input)
        
        # 4. Stress Score Calculation (Logic based on inputs)
        # Hum stress factors ko add kar rahe hain aur positive factors ko minus
        raw_score = (pressure * 10) + (examfear * 10) + (financial * 10) - (sleep * 5) - (family * 5)
        # Score ko 0-100 ki range mein laane ke liye normalization
        stress_score = max(0, min(100, raw_score + 40)) 

        st.markdown("---")
        st.subheader("Analysis Results")

        # Display Stress Level based on Score
        if stress_score <= 30:
            st.success(f"Stress Level: Low ({stress_score}%)")
            st.write("You are doing well!")
        elif stress_score <= 65:
            st.warning(f"Stress Level: Moderate ({stress_score}%)")
            st.write("You are under some pressure. Take it easy.")
        else:
            st.error(f"Stress Level: High ({stress_score}%)")
            st.write("Please take a break and seek support.")

        # Display Model Result
        if prediction[0] == 1:
            st.error("Model Prediction: Student is Stressed")
        else:
            st.success("Model Prediction: Student is Not Stressed")

        # 5. Personalized Suggestions
        st.subheader("Personalized Suggestions")

        if sleep < 6:
            st.write("• Maintain a proper sleep schedule (at least 7-8 hours).")
        if study > 8:
            st.write("• Take regular breaks during study time.")
        if social > 5:
            st.write("• Limit your social media usage to save mental energy.")
        if pressure > 3:
            st.write("• Break your academic tasks into smaller, manageable steps.")
        if family < 3:
            st.write("• Try to connect with friends or mentors for emotional support.")
        if activity < 2:
            st.write("• Add at least 20 mins of physical activity to your daily routine.")
        if screen > 7:
            st.write("• High screen time detected. Use blue light filters and take eye breaks.")
        if financial > 3:
            st.write("• Don't stress alone; discuss financial concerns with a trusted person.")
        if examfear > 3:
            st.write("• Practice mock tests to build confidence and reduce anxiety.")
        if timemanagement < 3:
            st.write("• Follow a structured daily schedule.")
