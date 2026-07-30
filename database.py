import sqlite3
import json
import os

def create_database():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/meetings.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            summary TEXT,
            opportunity_score INTEGER,
            followup_email TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meeting_insights (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER,
            pain_points TEXT,
            buying_signals TEXT,
            objections TEXT,
            next_steps TEXT,
            FOREIGN KEY(meeting_id) REFERENCES meetings(id)
        )
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER,
            task TEXT,
            description TEXT,
            priority TEXT,
            deadline TEXT,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY(meeting_id) REFERENCES meetings(id)
        )
        """)

    conn.commit()
    conn.close()
    
def save_meeting(result):

    conn = sqlite3.connect("database/meetings.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO meetings(
            company_name,
            summary,
            opportunity_score,
            followup_email
        )
        VALUES (?,?,?,?)
        """,
    (
        result.get("company_name", "Unknown"),
        result.get("meeting_summary", "No summary available"),
        result.get("opportunity_score", 0),
        result.get("followup_email", ""),
    
    ))
    meeting_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO meeting_insights(
            meeting_id,
            pain_points,
            buying_signals,
            objections,
            next_steps
        )
        VALUES (?,?,?,?,?)
    """,
    (
        meeting_id,
        json.dumps(result.get("pain_points", [])),
        json.dumps(result.get("buying_signals", [])),
        json.dumps(result.get("objections", [])),
        json.dumps(result.get("recommended_next_steps", [])),
    ))

    tasks = result.get("tasks", [])
    for task in tasks:

        cursor.execute("""
            INSERT INTO tasks(
                meeting_id,
                task,
                description,
                priority,
                deadline
            )
            VALUES (?,?,?,?,?)
        """,
        (
            meeting_id,
            task["task"],
            task["description"],
            task["priority"],
            task["deadline"],
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