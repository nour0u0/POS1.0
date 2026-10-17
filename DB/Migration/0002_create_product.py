import sqlite3

DB_PATH = "DB/DataBase.sqlite"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    designation TEXT,
    selling_price REAL NOT NULL DEFAULT 0,
    cost REAL NOT NULL DEFAULT 0,
    qte INTEGER NOT NULL DEFAULT 0,
    is_displayed INTEGER NOT NULL DEFAULT 1
)
""")

conn.commit()
conn.close()

