import sqlite3
import requests
import json

DB = "companion.db"

def create_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embed",
        json = {
            "model": "all-minilm",
            "input": text
            },
        timeout=30
        )
    
    response.raise_for_status()
    
    data = response.json()
    
    return data["embeddings"][0]

def initialize():
    conn = sqlite3.connect(DB)
    
    conn.enable_load_extension(True)
    conn.load_extension("./vec0.so")
    
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
    
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS memory_vectors
        USING vec0(
            memory_id INTEGER PRIMARY KEY,
            embedding FLOAT[384]
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
    embedding = create_embedding(content)
    
    
    conn = sqlite3.connect(DB)
    
    
    conn.enable_load_extension(True)
    conn.load_extension("./vec0.so")
     
    cursor = conn.execute(
        "INSERT INTO memories (content) VALUES (?)",
        (content,)
    )
    
    memory_id = cursor.lastrowid
    
    conn.execute(
        """

        INSERT INTO memory_vectors (memory_id, embedding)
        VALUES (?, ?)
        """,
        (memory_id, json.dumps(embedding))
    )
    
    conn.commit()
    conn.close()
    
def search_memories(query, limit=5):
    embedding = create_embedding(query)
    
    conn = sqlite3.connect(DB)
    
    conn.enable_load_extension(True)
    conn.load_extension("./vec0.so")
    
    vector_json = json.dumps(embedding)
    
    rows = conn.execute("""
        SELECT memory_id, distance
        FROM memory_vectors
        WHERE embedding MATCH ?
            AND k = ?
        ORDER BY distance
    """, (vector_json, limit)).fetchall()
                        
        
    memories = []
    
    for memory_id, distance in rows:
        row = conn.execute(
            "SELECT content FROM memories WHERE id = ?",
            (memory_id,)
        ).fetchone()
        
        if row:
            memories.append(row[0])
            
    conn.close()
    
    return memories
    