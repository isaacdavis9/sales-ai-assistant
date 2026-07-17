from ai_engine import analyze_transcript

def read_txt(uploaded_file):
    transcript = uploaded_file.read().decode("utf-8")
    return transcript

def parse_transcript(uploaded_file):
    transcript = read_txt(uploaded_file)
    return analyze_transcript(transcript)