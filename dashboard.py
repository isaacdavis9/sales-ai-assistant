import streamlit as st
from database import get_all_meetings, get_total_meetings, get_average_score, get_highest_score, get_company_count
import plotly.express as px
import pandas as pd

def show_dashboard():

    st.title("Sales AI Dashboard")
    st.caption("AI-powered meeting analytics and sales insights")

    st.divider()

    meetings = get_all_meetings()

    df = pd.DataFrame(
            meetings, 
            columns=[
                "ID", 
                "Company Name", 
                "Summary", 
                "Pain Points",
                "Buying Signals",
                "Objections",
                "Recommended Next Steps",
                "Opportunity Score",
                "Follow-up Email"
            ]
        )
    
    if not meetings:
        st.info("No meetings analyzed yet.")
        return

    total_meetings = len(meetings)

    scores = []

    for meeting in meetings:
        scores.append(meeting[7])

    average_score = sum(scores) / len(scores)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Meetings",
        get_total_meetings()
    )

    col2.metric(
        "Average Opportunity Score",
        f"{get_average_score()}%"
    )

    col3.metric(
        "Highest Score",
        f"{get_highest_score()}%"
    )

    col4.metric(
        "Companies",
        get_company_count()
    )

    st.divider()

    st.subheader("Recent Meetings")

    st.dataframe(
        df[["Company Name", "Opportunity Score"]],
        use_container_width=True
        )
    
    st.divider()

    fig = px.histogram(
        df,
        x="Opportunity Score",
        nbins=10,
        title="Opportunity Score Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)