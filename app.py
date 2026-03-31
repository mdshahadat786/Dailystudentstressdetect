import streamlit as st
import pickle
import numpy as np

# Page configuration
st.set_page_config(page_title="Stress Detection", layout="centered")

# Title and introduction
st.title("Student Stress Detection System")
st.write("Please share your daily routine and feelings. I will help you understand your current stress level.")

# Load the pre-trained machine learning model
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    st.success("System is ready to help you! ✅")
except Exception as e:
    st.error("Error: Model file not found. Please ensure 'model.pkl' is in the folder.")
    st.stop()

# Input Section for student metrics
st.header("Enter Student Details")

# Sliders for various life and academic factors
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

# Calculate total hours to ensure data is realistic
total_hours = study + sleep + social + activity + extra

# Action button to trigger prediction
if st.button("Predict Stress"):
    # Check if the total hours exceed a 24-hour day
    if total_hours > 24:
        st.warning(f"⚠️ **Data Alert:** You have logged {total_hours} hours. A day only has 24 hours.")
    else:
        # 1. Prepare the feature array for the model
        data_input = np.array([[study, sleep, social, pressure, family,
                                activity, screen, extra, financial,
                                examfear, timemanagement]])

        # 2. Execute model prediction (Mandatory Background Step)
        prediction_val = model.predict(data_input)[0]
        
        # 3. Calculate a manual Stress Score for detailed intensity
        # Factors like pressure increase the score, while sleep and family support decrease it
        raw_score = (pressure * 10) + (examfear * 10) + (financial * 10) - (sleep * 5) - (family * 5)
        
        # Normalize the score within the 0 to 100 range
        stress_score = max(0, min(100, raw_score + 40)) 

        # 4. Hybrid Logic: Ensure the status matches the high intensity score
        # If score is high or model predicts 1, set status to Stressed
        if stress_score > 50 or prediction_val == 1:
            status = "Stressed"
        else:
            status = "Not Stressed"

        st.markdown("---")
        st.subheader("Analysis Results")

        # Natural phrasing for the result display
        st.info(f"📋 **System Observation:** Student is **{status}**")

        # Categorized display based on the stress score
        if stress_score <= 30:
            st.success(f"Stress Level: Low ({stress_score}%)")
            st.write("You are doing well!")
        elif stress_score <= 65:
            st.warning(f"Stress Level: Moderate ({stress_score}%)")
            st.write("You are under some pressure. Take it easy.")
        else:
            st.error(f"Stress Level: High ({stress_score}%)")
            st.write("Please take a break and seek support.")

        # 5. Provide personalized feedback based on individual sliders
        st.subheader("Personalized Suggestions")
        if sleep < 6: 
            st.write("• Maintain a proper sleep schedule (at least 7-8 hours).")
        if study > 8: 
            st.write("• Take regular breaks during study time.")
        if pressure > 3: 
            st.write("• Break your academic tasks into smaller steps.")
        if financial > 3: 
            st.write("• Discuss financial concerns with a trusted person.")
        if examfear > 3: 
            st.write("• Practice mock tests to build confidence.")
        if timemanagement < 3: 
            st.write("• Follow a structured daily schedule.")
