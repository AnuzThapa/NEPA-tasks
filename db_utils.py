# db_utils.py
import sqlite3
from typing import List, Dict

DB_PATH = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_message(conversation_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (conversation_id, role, content) 
        VALUES (?, ?, ?)
    """, (conversation_id, role, content))
    conn.commit()
    conn.close()

def load_last_messages(conversation_id: str, N: int) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content FROM messages
        WHERE conversation_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (conversation_id, N))
    rows = cursor.fetchall()
    conn.close()
    # Return in chronological order
    return [{"role": role, "content": content} for role, content in reversed(rows)]
