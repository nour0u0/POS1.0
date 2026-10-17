import sqlite3


class InvoiceItem:

    DB_PATH = "DB/DataBase.sqlite"

    def __init__(
        self,
        id=None,
        invoice_id=None,
        name=None,
        designation=None,
        selling_price=0,
        cost=0,
        qte=0,
        is_displayed=1,
        db_path=None
    ):
        self.db_path = db_path or self.DB_PATH

        self.id = id
        self.invoice_id = invoice_id
        self.name = name
        self.designation = designation
        self.selling_price = selling_price
        self.cost = cost
        self.qte = qte
        self.is_displayed = is_displayed

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
            invoice_id=row[1],
            name=row[2],
            designation=row[3],
            selling_price=row[4],
            cost=row[5],
            qte=row[6],
            is_displayed=row[7],
            db_path=db_path
        )

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    def create(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO invoice_items
            (
                invoice_id,
                name,
                designation,
                selling_price,
                cost,
                qte,
                is_displayed
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.invoice_id,
            self.name,
            self.designation,
            self.selling_price,
            self.cost,
            self.qte,
            self.is_displayed
        ))

        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

        return self

    def update(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE invoice_items
            SET
                name = ?,
                designation = ?,
                selling_price = ?,
                cost = ?,
                qte = ?,
                is_displayed = ?
            WHERE id = ?
        """, (
            self.name,
            self.designation,
            self.selling_price,
            self.cost,
            self.qte,
            self.is_displayed,
            self.id
        ))

        conn.commit()
        conn.close()

    def delete(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM invoice_items WHERE id = ?",
            (self.id,)
        )

        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    @classmethod
    def get_by_id(cls, item_id, db_path=None):
        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM invoice_items WHERE id = ?",
            (item_id,)
        )

        row = cursor.fetchone()
        conn.close()

        return cls.from_row(row, db)

    @classmethod
    def get_by_invoice(cls, invoice_id, db_path=None):
        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM invoice_items
            WHERE invoice_id = ?
            ORDER BY id
        """, (invoice_id,))

        rows = cursor.fetchall()
        conn.close()

        return [cls.from_row(row, db) for row in rows]

    @classmethod
    def delete_by_invoice(cls, invoice_id, db_path=None):
        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM invoice_items
            WHERE invoice_id = ?
        """, (invoice_id,))

        conn.commit()
        conn.close()