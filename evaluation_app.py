import streamlit as st
import pandas as pd
import joblib
import certifi

from feedback_engine import generate_feedback
from database.mongodb_connection import students_collection
from report_generator import generate_pdf

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(page_title="InternML System", layout="wide")

st.title("🚀 InternML – ML Based Internship Performance Evaluation System")

st.write("AI system to evaluate student internship performance and predict success probability.")

# -----------------------------
# Load ML Model
# -----------------------------

model = joblib.load("model.pkl")

# -----------------------------
# Individual Student Evaluation
# -----------------------------

st.header("👤 Individual Student Evaluation")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Student Name")

    coding = st.slider(
        "Coding Skill Level",
        1,
        5
    )

    projects = st.number_input(
        "Projects Completed",
        0,
        10
    )

with col2:

    hours = st.number_input(
        "Hours Spent Per Week",
        0,
        50
    )

    attendance = st.slider(
        "Attendance %",
        0,
        100
    )

    domain = st.selectbox(
        "Preferred Domain",
        ["", "AI", "ML", "Frontend", "Backend"]
    )

# -----------------------------
# Evaluate Button
# -----------------------------

if st.button("Evaluate Student"):

    # Prepare dataframe to avoid sklearn warning
    input_df = pd.DataFrame({
        "coding_skill":[coding],
        "hours_spent":[hours],
        "projects_completed":[projects],
        "attendance":[attendance]
    })

    prediction = model.predict(input_df)

    probability = model.predict_proba(input_df)

    # -----------------------------
    # Score Calculation
    # -----------------------------

    score = (coding * 15) + (hours * 2) + (projects * 15) + (attendance * 0.5)

    percentage = min(score,100)

    st.subheader("🎯 Performance Score")

    st.success(f"{percentage}%")

    success_prob = probability[0][1] * 100

    st.subheader("📈 Success Probability")

    st.info(f"{success_prob:.2f}%")

    # -----------------------------
    # Prediction Result
    # -----------------------------

    if prediction[0] == 1:

        st.success("Prediction: Student likely to successfully complete internship")

        certificate = "Eligible for Certificate"

    else:

        st.error("Prediction: Student needs improvement")

        certificate = "Not Eligible Yet"

    st.subheader("🏅 Certificate Status")

    st.write(certificate)

    # -----------------------------
    # AI Feedback
    # -----------------------------

    feedback = generate_feedback(
        coding,
        hours,
        projects,
        attendance,
        domain
    )

    st.subheader("🧠 AI Generated Feedback")

    st.text_area(
        "Feedback",
        feedback,
        height=150
    )

    # -----------------------------
    # Save to MongoDB
    # -----------------------------

    student_data = {

        "name": name,
        "coding_skill": coding,
        "hours_spent": hours,
        "projects_completed": projects,
        "attendance": attendance,
        "domain": domain,
        "score": percentage,
        "prediction": int(prediction[0]),
        "feedback": feedback
    }

    try:

        students_collection.insert_one(student_data)

        st.success("Student evaluation saved in MongoDB")

    except:

        st.warning("MongoDB not connected. Data not saved.")

    # -----------------------------
    # Generate PDF Report
    # -----------------------------

    pdf_file = generate_pdf(
        name,
        percentage,
        certificate,
        feedback
    )

    with open(pdf_file,"rb") as f:

        st.download_button(

            label="📄 Download Evaluation Report",

            data=f,

            file_name=pdf_file,

            mime="application/pdf"
        )

# -----------------------------
# Batch Upload Evaluation
# -----------------------------

st.header("📂 Batch Dataset Evaluation")

uploaded_files = st.file_uploader(

    "Upload CSV files",

    type="csv",

    accept_multiple_files=True
)

if uploaded_files:

    st.write("Processing datasets...")

    for f in uploaded_files:

        df = pd.read_csv(f)

        for idx,row in df.iterrows():

            coding = row["coding_skill"]
            projects = row["projects_completed"]
            hours = row["hours_spent"]
            attendance = row["attendance"]

            name = row.get("name",f"Student_{idx}")

            domain = row.get("domain","")

            input_df = pd.DataFrame({
                "coding_skill":[coding],
                "hours_spent":[hours],
                "projects_completed":[projects],
                "attendance":[attendance]
            })

            prediction = model.predict(input_df)

            score = (coding * 15) + (hours * 2) + (projects * 15) + (attendance * 0.5)

            percentage = min(score,100)

            feedback = generate_feedback(

                coding,
                hours,
                projects,
                attendance,
                domain
            )

            student_data = {

                "name": name,
                "coding_skill": coding,
                "hours_spent": hours,
                "projects_completed": projects,
                "attendance": attendance,
                "domain": domain,
                "score": percentage,
                "prediction": int(prediction[0]),
                "feedback": feedback
            }

            try:

                students_collection.insert_one(student_data)

            except:

                pass

    st.success("Batch evaluation completed")

# -----------------------------
# Student Dashboard
# -----------------------------

st.header("📊 Student Evaluation Dashboard")

if st.button("Show All Student Records"):

    try:

        records = list(

            students_collection.find(

                {},

                {"_id":0}
            )

        )

        if records:

            df = pd.DataFrame(records)

            st.dataframe(df)

        else:

            st.info("No records found")

    except:

        st.warning("MongoDB connection not available")