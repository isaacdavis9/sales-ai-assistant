import streamlit as st
from ai_engine import analyze_transcript
from database import create_database
from database import save_meeting
from transcript_parser import read_txt
from email_generator import generate_followup_email
from  task_generator import generate_tasks
from dashboard import show_dashboard

create_database()

st.title("Sales AI Assistant")
st.subheader("Use the sidebar to navigate between different sections.")
page = st.sidebar.selectbox(
    "Navigation",
    [
        "Title Page",
        "Analyze Meeting",
        "Dashboard"
    ]
)

if page == "Analyze Meeting":
    st.write(
    "Upload a customer meeting transcript and receive AI-powered insights."
    )
    uploaded_file = st.file_uploader(
        "Upload Transcript",
        type=["txt"]
    )

    if uploaded_file:
        transcript = read_txt(uploaded_file)
        st.subheader("Transcript Preview")
        st.write(transcript)

        if st.button("Analyze Meeting"):
            result = analyze_transcript(transcript)
            email = generate_followup_email(result)
            tasks = generate_tasks(result)

            result["followup_email"] = email
            result["tasks"] = tasks
            
            save_meeting(result)

            st.subheader("AI Analysis")
            st.json(result)

            st.subheader("Generated Follow-up Email")
            st.write(email)

            st.subheader("Recommended Tasks")
            for task in tasks:
                st.write("### " + task["task"])

                st.write(
                    "Priority:",
                    task["priority"]
                )
                st.write(
                    "Deadline:",
                    task["deadline"]
                )
                st.write(
                    task["description"]
                )
                st.divider()
            
if page == "Dashboard":
    show_dashboard()