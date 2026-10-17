import sqlite3

DB_PATH = "DB/DataBase.sqlite"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoice_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER NOT NULL,

    name TEXT NOT NULL,
    designation TEXT,
    selling_price REAL NOT NULL,
    cost REAL NOT NULL,
    qte INTEGER NOT NULL,
    is_displayed INTEGER NOT NULL,

    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()