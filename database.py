import sqlite3
import json

def create_database():
    conn = sqlite3.connect("database/meetings.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            summary TEXT,
            pain_points TEXT,
            buying_signals TEXT,
            objections TEXT,
            next_steps TEXT,
            opportunity_score INTEGER,
            followup_email TEXT
        )
    """)
    conn.commit()
    conn.close()
    
def save_meeting(result):

    conn = sqlite3.connect("database/meetings.db")
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO meetings(
            customer_name,
            summary,
            pain_points,
            buying_signals,
            objections,
            next_steps,
            opportunity_score
        )
        VALUES (?,?,?,?,?,?,?)

        """,
    (
        result.get("company_name", "Unknown"),
        result.get("meeting_summary", "No summary available"),
        json.dumps(result.get("pain_points", [])),
        json.dumps(result.get("buying_signals", [])),
        json.dumps(result.get("objections", [])),
        json.dumps(result.get("recommended_next_steps", [])),
        result.get("opportunity_score", 0),
    ))

    conn.commit()
    conn.close()
    

def get_all_meetings():

    conn = sqlite3.connect("database/meetings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meetings")
    rows = cursor.fetchall()
    conn.close()
    
    return rows

def get_meeting(id):
    conn = sqlite3.connect("database/meetings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meetings WHERE id=?", (id,))
    row = cursor.fetchone()
    conn.close()

    return row


def get_total_meetings():
    conn = sqlite3.connect("database/meetings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM meetings")
    total = cursor.fetchone()[0]
    conn.close()

    return total

def get_average_score():
    conn = sqlite3.connect("database/meetings.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT AVG(opportunity_score) 
    FROM meetings
    """)
    average = cursor.fetchone()[0]
    conn.close()

    return round(average or 0, 1)

def get_highest_score():
    conn = sqlite3.connect("database/meetings.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT MAX(opportunity_score) 
    FROM meetings
    """)
    highest = cursor.fetchone()[0]
    conn.close()

    return highest or 0

def get_company_count():
    conn = sqlite3.connect("database/meetings.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(DISTINCT customer_name) 
    FROM meetings
    """)
    count = cursor.fetchone()[0]
    conn.close()

    return count