import streamlit as st
from database import get_all_meetings

def show_dashboard():

    st.title("Sales AI Dashboard")
    meetings = get_all_meetings()

    if not meetings:
        st.info("No meetings analyzed yet.")
        return

    total_meetings = len(meetings)

    scores = []

    for meeting in meetings:
        scores.append(meeting[7])

    average_score = sum(scores) / len(scores)

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Meetings",
            total_meetings
        )

    with col2:
        st.metric(
            "Average Opportunity Score",
            round(average_score)
        )

    st.divider()

    st.subheader("Recent Meetings")

    for meeting in meetings[::-1]:
        st.write(
            f"""
            ### {meeting[1]}

            Opportunity Score:
            {meeting[7]}

            Summary:
            {meeting[2]}
            """
        )
        st.divider()