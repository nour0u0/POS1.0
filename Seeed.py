import sqlite3

DB_PATH = "DB/DataBase.sqlite"


def seed():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    # Check if admin already exists
    cursor.execute("""
        SELECT id
        FROM users
        WHERE username = ?
    """, ("admin",))


    existing = cursor.fetchone()


    if existing:
        print("Admin user already exists")
        conn.close()
        return


    # Create admin user
    cursor.execute("""
        INSERT INTO users
        (
            username,
            password,
            role
        )
        VALUES (?, ?, ?)
    """, (
        "admin",
        "admin",
        "admin"
    ))


    conn.commit()
    conn.close()

    print("Admin user created successfully")


if __name__ == "__main__":
    seed()