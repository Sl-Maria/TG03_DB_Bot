import sqlite3

conn = sqlite3.connect('school_data.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL
)""")

conn.commit()
conn.close()
