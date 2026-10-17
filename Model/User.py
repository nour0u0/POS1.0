import sqlite3


class User:

    DB_PATH = "DB/DataBase.sqlite"

    def __init__(
        self,
        id=None,
        username=None,
        password=None,
        role=None,
        created_at=None,
        db_path=None
    ):
        self.db_path = db_path or self.DB_PATH

        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.created_at = created_at

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _connect(self):
        return sqlite3.connect(self.db_path)

    @classmethod
    def from_row(cls, row, db_path=None):
        if row is None:
            return None

        return cls(
            id=row[0],
            username=row[1],
            password=row[2],
            role=row[3],
            created_at=row[4],
            db_path=db_path
        )

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def create(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (
            self.username,
            self.password,
            self.role
        ))

        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

        return self

    def update(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET username = ?, password = ?, role = ?
            WHERE id = ?
        """, (
            self.username,
            self.password,
            self.role,
            self.id
        ))

        conn.commit()
        conn.close()

    def delete(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id = ?",
            (self.id,)
        )

        conn.commit()
        conn.close()

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    @classmethod
    def get_by_id(cls, user_id, db_path=None):
        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )

        row = cursor.fetchone()
        conn.close()

        return cls.from_row(row, db)

    @classmethod
    def get_by_username(cls, username, db_path=None):
        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        row = cursor.fetchone()
        conn.close()

        return cls.from_row(row, db)

    @classmethod
    def get_all(cls, db_path=None):
        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users ORDER BY username"
        )

        rows = cursor.fetchall()
        conn.close()

        return [cls.from_row(row, db) for row in rows]

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    @classmethod
    def authenticate(cls, username, password, db_path=None):
        """
        Returns the User object if the credentials are correct,
        otherwise returns None.
        """
        user = cls.get_by_username(username, db_path)

        if user is None:
            return None

        if user.password != password:
            return None

        return user

    @classmethod
    def username_exists(cls, username, db_path=None):
        return cls.get_by_username(username, db_path) is not None

    @classmethod
    def create_user(cls, username, password, role="caissier", db_path=None):
        if cls.username_exists(username, db_path):
            raise ValueError("Username already exists.")

        user = cls(
            username=username,
            password=password,
            role=role,
            db_path=db_path
        )

        return user.create()