import sqlite3

conn = sqlite3.connect("chat.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM chats")
rows = cursor.fetchall()

for row in rows:
    print("\n----------------------")
    print(f"ID: {row[0]}")
    print(f"User ID: {row[1]}")
    print(f"User Message: {row[2]}")
    print(f"Bot Response: {row[3]}")
    print(f"Time: {row[4]}")