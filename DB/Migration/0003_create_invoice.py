import sqlite3

DB_PATH = "DB/DataBase.sqlite"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_price REAL NOT NULL DEFAULT 0,
    profit REAL NOT NULL DEFAULT 0
)
""")

conn.commit()
conn.close()