from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_tasks(meeting_analysis):
    prompt = f"""
You are an expert sales operations assistant.

Analyze this customer meeting and create actionable CRM tasks.
For each task provide:

- task name
- description
- priority (High, Medium, Low)
- suggested deadline

Return ONLY valid JSON.

Use this format:
[
    {{
        "task": "",
        "description": "",
        "priority": "",
        "deadline": ""
    }}
]
Meeting Information:

Company:
{meeting_analysis.get("company_name")}
Summary:
{meeting_analysis.get("meeting_summary")}
Pain Points:
{meeting_analysis.get("pain_points")}
Buying Signals:
{meeting_analysis.get("buying_signals")}
Recommended Next Steps:
{meeting_analysis.get("recommended_next_steps")}
"""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return json.loads(response.output_text)