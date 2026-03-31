import streamlit as st
import pickle
import numpy as np

# Page configuration
st.set_page_config(page_title="Stress Detection", layout="centered")

# Title
st.title("Student Stress Detection System")
st.write("Please share your daily routine and feelings. I will help you understand your current stress level.")

# Load model
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    st.success("System is ready to help you! ✅")
except Exception as e:
    st.error("Error: Model file not found. Please ensure 'model.pkl' is in the folder.")
    st.stop()

# Input Section
st.header("Enter Student Details")

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

total_hours = study + sleep + social + activity + extra

if st.button("Predict Stress"):
    if total_hours > 24:
        st.warning(f"⚠️ **Data Alert:** You have logged {total_hours} hours. A day only has 24 hours.")
    else:
        # 1. Prepare data for model
        data_input = np.array([[study, sleep, social, pressure, family,
                                activity, screen, extra, financial,
                                examfear, timemanagement]])

        # 2. Model Prediction (Background)
        prediction_val = model.predict(data_input)[0]
        
        # 3. Stress Score Calculation (Logic based on inputs)
        raw_score = (pressure * 10) + (examfear * 10) + (financial * 10) - (sleep * 5) - (family * 5)
        stress_score = max(0, min(100, raw_score + 40)) 

        # 4. FIX: Synchronizing Model with Score (Hybrid Logic)
        # Agar stress_score 50% se zyada hai, toh AI status "Stressed" hi dikhayega
        if stress_score > 50 or prediction_val == 1:
            status = "Stressed"
        else:
            status = "Not Stressed"

        st.markdown("---")
        st.subheader("Analysis Results")

        # DISPLAY AI STATUS (Ab ye score ke saath match karega)
        st.info(f"🤖 **AI Prediction:** Student is **{status}**")

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

        # 5. Personalized Suggestions
        st.subheader("Personalized Suggestions")
        if sleep < 6: st.write("• Maintain a proper sleep schedule (at least 7-8 hours).")
        if study > 8: st.write("• Take regular breaks during study time.")
        if pressure > 3: st.write("• Break your academic tasks into smaller steps.")
        if financial > 3: st.write("• Discuss financial concerns with a trusted person.")
        if examfear > 3: st.write("• Practice mock tests to build confidence.")
        if timemanagement < 3: st.write("• Follow a structured daily schedule.")
