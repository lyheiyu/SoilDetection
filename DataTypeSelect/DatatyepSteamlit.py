# streamlit_app.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="SOILCRATES Data Uploader", layout="centered")

st.title("📊 SOILCRATES Work Package Data Uploader")

# 可选的数据类型
data_type = st.selectbox(
    "Select data type to upload",
    [
        "WP1 - Living Lab Participation",
        "WP2 - Pilot Projects",
        "WP3 - Socio-Economic Impact",
        "WP4 - Soil Monitoring Indicators",
        "WP5 - Soil Techniques & Ecosystem",
        "WP6 - Communication & Engagement",
        "WP7 - Project Management"
    ]
)

st.markdown("---")

# 定义不同 WP 类型的上传接口
if data_type == "WP1 - Living Lab Participation":
    st.subheader("Upload stakeholder list (CSV)")
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview:")
        st.dataframe(df)

elif data_type == "WP2 - Pilot Projects":
    st.subheader("Upload project proposal (PDF or DOCX)")
    uploaded_file = st.file_uploader("Upload proposal document", type=["pdf", "docx"])
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

elif data_type == "WP3 - Socio-Economic Impact":
    st.subheader("Upload impact assessment data")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.dataframe(df)

elif data_type == "WP4 - Soil Monitoring Indicators":
    st.subheader("Upload multiple sensor files")
    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    for file in uploaded_files:
        st.write(f"📄 {file.name}")
        df = pd.read_csv(file)
        st.dataframe(df.head())

elif data_type == "WP5 - Soil Techniques & Ecosystem":
    st.subheader("Describe the soil technique used")
    title = st.text_input("Technique Title")
    description = st.text_area("Description")
    file = st.file_uploader("Upload related file (optional)", type=["pdf", "csv"])
    if st.button("Submit"):
        st.success("Technique submitted!")

elif data_type == "WP6 - Communication & Engagement":
    st.subheader("Upload outreach event details")
    name = st.text_input("Event Title")
    date = st.date_input("Date of the event")
    participants = st.number_input("Number of participants", min_value=1)
    if st.button("Submit Event"):
        st.success("Event data submitted.")

elif data_type == "WP7 - Project Management":
    st.subheader("Upload project report or quality data")
    file = st.file_uploader("Upload project document", type=["pdf", "docx", "csv"])
    if file:
        st.success(f"Uploaded: {file.name}")

