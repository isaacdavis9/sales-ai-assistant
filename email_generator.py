from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_followup_email(meeting_analysis):
    prompt = f"""
You are a professional enterprise sales representative.
Write a personalized follow-up email based on this customer meeting.

The email should:

- Thank the customer for their time
- Summarize important discussion points
- Address customer pain points
- Reinforce value
- Clearly state next steps
- Maintain a professional but friendly tone

Meeting Information:

Company:
{meeting_analysis.get("company_name")}
Summary:
{meeting_analysis.get("meeting_summary")}
Pain Points:
{meeting_analysis.get("pain_points")}
Buying Signals:
{meeting_analysis.get("buying_signals")}
Next Steps:
{meeting_analysis.get("recommended_next_steps")}

Return only the email text.
"""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text