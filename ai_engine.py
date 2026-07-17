from openai import OpenAI
from config import OPENAI_API_KEY
import json

client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_transcript(transcript):
    prompt = f"""
You are an expert Salesforce Sales analyst.
Analayze this customer meeting transcript.

Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.
Do not explain anything.
Return exactly this schema:

Provide:
- Name of company
- Meeting summary 
- Customer pain points
- Buying signals 
- Objections
- Recommended next steps
- Opportunity score

Use this format:
{{
    "company_name": "",
    "meeting_summary": "",
    "pain_points": [],
    "buying_signals": [], 
    "objections": [],
    "recommended_next_steps": [],
    "opportunity_score": 0,
}}

Transcript: 
{transcript}
"""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return json.loads(response.output_text)