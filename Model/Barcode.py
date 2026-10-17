import sqlite3


class Barcode:

    DB_PATH = "DB/DataBase.sqlite"


    def __init__(
        self,
        id=None,
        product_id=None,
        barcode=None,
        db_path=None
    ):

        self.db_path = db_path or self.DB_PATH

        self.id = id
        self.product_id = product_id
        self.barcode = barcode


    def _connect(self):
        return sqlite3.connect(self.db_path)


    @classmethod
    def from_row(cls, row, db_path=None):

        if row is None:
            return None

        return cls(
            id=row[0],
            product_id=row[1],
            barcode=row[2],
            db_path=db_path
        )


    def create(self):

        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO barcodes
            (
                product_id,
                barcode
            )
            VALUES (?, ?)
        """, (
            self.product_id,
            self.barcode
        ))

        conn.commit()

        self.id = cursor.lastrowid

        conn.close()

        return self


    def update(self):

        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE barcodes
            SET barcode = ?
            WHERE id = ?
        """, (
            self.barcode,
            self.id
        ))

        conn.commit()
        conn.close()


    def delete(self):

        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM barcodes
            WHERE id = ?
        """, (
            self.id,
        ))

        conn.commit()
        conn.close()


    @classmethod
    def get_by_id(cls, barcode_id, db_path=None):

        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM barcodes
            WHERE id = ?
        """, (
            barcode_id,
        ))

        row = cursor.fetchone()

        conn.close()

        return cls.from_row(row, db)


    @classmethod
    def get_by_product(cls, product_id, db_path=None):

        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM barcodes
            WHERE product_id = ?
        """, (
            product_id,
        ))

        rows = cursor.fetchall()

        conn.close()

        return [
            cls.from_row(row, db)
            for row in rows
        ]
    @classmethod
    def get_product_by_barcode(cls, barcode):

        conn = sqlite3.connect(
            cls.DB_PATH
        )

        cursor = conn.cursor()


        cursor.execute("""
            SELECT product_id
            FROM barcodes
            WHERE barcode=?
        """,(barcode,))


        result = cursor.fetchone()

        conn.close()


        if result:
            return result[0]

        return None