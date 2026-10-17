import sqlite3


class Invoice:

    DB_PATH = "DB/DataBase.sqlite"

    def __init__(
        self,
        id=None,
        date=None,
        total_price=0,
        profit=0,
        db_path=None
    ):
        self.db_path = db_path or self.DB_PATH

        self.id = id
        self.date = date
        self.total_price = total_price
        self.profit = profit

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _connect(self):
        return sqlite3.connect(self.db_path)

    @classmethod
    def from_row(cls, row, db_path=None):
        if row is None:
            return None

        return cls(
            id=row[0],
            date=row[1],
            total_price=row[2],
            profit=row[3],
            db_path=db_path
        )

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    def create(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO invoices (total_price, profit)
            VALUES (?, ?)
        """, (
            self.total_price,
            self.profit
        ))

        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

        return self

    def update(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE invoices
            SET
                total_price = ?,
                profit = ?
            WHERE id = ?
        """, (
            self.total_price,
            self.profit,
            self.id
        ))

        conn.commit()
        conn.close()
    def delete(self):

        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()


        # Delete invoice items first
        cursor.execute("""
            DELETE FROM invoice_items
            WHERE invoice_id = ?
        """, (
            self.id,
        ))


        # Delete invoice
        cursor.execute("""
            DELETE FROM invoices
            WHERE id = ?
        """, (
            self.id,
        ))


        conn.commit()

        conn.close()
    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    @classmethod
    def get_by_id(cls, invoice_id, db_path=None):
        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM invoices WHERE id = ?",
            (invoice_id,)
        )

        row = cursor.fetchone()
        conn.close()

        return cls.from_row(row, db)

    @classmethod
    def get_all(cls, db_path=None):
        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM invoices
            ORDER BY date DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [cls.from_row(row, db) for row in rows]
    @classmethod
    def get_by_date_range(cls, start, end):

        conn = sqlite3.connect(
            cls.DB_PATH
        )

        cursor = conn.cursor()


        cursor.execute("""
            SELECT *
            FROM invoices
            WHERE date(date) BETWEEN date(?) AND date(?)
            ORDER BY date DESC
        """, (
            start,
            end
        ))


        rows = cursor.fetchall()

        conn.close()


        return [
            cls.from_row(row)
            for row in rows
        ]
    @classmethod
    def get_last(cls):

        conn = sqlite3.connect(
            cls.DB_PATH
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM invoices
            ORDER BY id DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        conn.close()


        if row:

            return cls.get_by_id(
                row[0]
            )

        return None
    @classmethod
    def get_next(cls, invoice_id):

        conn = sqlite3.connect(
            cls.DB_PATH
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM invoices
            WHERE id > ?
            ORDER BY id ASC
            LIMIT 1
        """,(
            invoice_id,
        ))


        row = cursor.fetchone()

        conn.close()


        if row:

            return cls.get_by_id(
                row[0]
            )


        return None
    @classmethod
    def get_previous(cls, invoice_id):

        conn = sqlite3.connect(
            cls.DB_PATH
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM invoices
            WHERE id < ?
            ORDER BY id DESC
            LIMIT 1
        """,(
            invoice_id,
        ))


        row = cursor.fetchone()

        conn.close()


        if row:

            return cls.get_by_id(
                row[0]
            )


        return None