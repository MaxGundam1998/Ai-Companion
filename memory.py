import sqlite3

DB = "companion.db"

def initialize():
    conn = sqlite3.connect(DB)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )
    """)
    
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )

    """)
    
    
    conn.commit()
    conn.close()
    

def save_message(role, content):
    conn = sqlite3.connect(DB)
    
    conn.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        (role, content)
       )
    
    conn.commit()
    conn.close()
    
def recent_message(limit=10):
    conn = sqlite3.connect(DB)
    
    rows = conn.execute("""
        SELECT role, content
        FROM messages
        ORDER BY id DESC
        LIMIT ?

    """, (limit,)).fetchall()
    conn.close()
    rows.reverse()
    
    return[
     {"role": role, "content": content}
     for role, content in rows
     ]


def save_memory(content):
    conn = sqlite3.connect(DB)
    
    conn.execute(
        "INSERT INTO memories (content) VALUES (?)",
        (content,)
    )
    
    conn.commit()
    conn.close()
    
def get_memories(limit=10):
    conn = sqlite3.connect(DB)
    
    rows = conn.execute("""
        SELECT content
        FROM memories
        ORDER by id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    
    conn.close()
    
    return [row[0] for row in rows]
    
    
    