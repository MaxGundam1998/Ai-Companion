import sqlite3

conn = sqlite3.connect("companion.db")

conn.execute("DELETE FROM messages")

conn.execute("DELETE FROM memories")

conn.execute("DELETE FROM sqlite_sequence WHERE name='messages'")
conn.execute("DELETE FROM sqlite_sequence WHERE name='memories'")

conn.commit()
conn.close()

print("Memory reset successful")