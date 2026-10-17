import sqlite3

DB_PATH = "DB/DataBase.sqlite"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS barcodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    barcode TEXT NOT NULL UNIQUE,

    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()