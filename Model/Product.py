import sqlite3

from Model.Barcode import Barcode
class Product:

    DB_PATH = "DB/DataBase.sqlite"

    def __init__(
        self,
        id=None,
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
            name=row[1],
            designation=row[2],
            selling_price=row[3],
            cost=row[4],
            qte=row[5],
            is_displayed=row[6],
            db_path=db_path
        )

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    def create(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO products
            (name, designation, selling_price, cost, qte, is_displayed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
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
            UPDATE products
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
            "DELETE FROM products WHERE id = ?",
            (self.id,)
        )

        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    @classmethod
    def get_by_id(cls, product_id, db_path=None):
        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
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
            "SELECT * FROM products ORDER BY name"
        )

        rows = cursor.fetchall()
        conn.close()

        return [cls.from_row(row, db) for row in rows]

    @classmethod
    def fetch_by_barcode(cls, barcode, db_path=None):
        """
        Returns the product associated with a barcode.
        """
        db = db_path or cls.DB_PATH

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.*
            FROM products p
            INNER JOIN barcodes b
                ON p.id = b.product_id
            WHERE b.barcode = ?
        """, (barcode,))

        row = cursor.fetchone()
        conn.close()

        return cls.from_row(row, db)
    @classmethod
    def search(
        cls,
        barcode=None,
        name=None,
        designation=None
    ):

        conn = sqlite3.connect(
            cls.DB_PATH
        )

        cursor = conn.cursor()


        # Search by barcode first
        if barcode:

            cursor.execute("""
                SELECT product_id
                FROM barcodes
                WHERE barcode LIKE ?
            """, (
                f"%{barcode}%",
            ))

            ids = cursor.fetchall()


            products = []


            for item in ids:

                product = cls.get_by_id(
                    item[0]
                )

                if product:
                    products.append(
                        product
                    )


            conn.close()

            return products



        # Search product fields

        query = """
            SELECT *
            FROM products
            WHERE 1=1
        """

        params = []


        if name:

            query += """
                AND name LIKE ?
            """

            params.append(
                f"%{name}%"
            )


        if designation:

            query += """
                AND designation LIKE ?
            """

            params.append(
                f"%{designation}%"
            )


        cursor.execute(
            query,
            params
        )


        rows = cursor.fetchall()

        conn.close()


        return [
            cls.from_row(row)
            for row in rows
        ]
    @classmethod
    def get_by_barcode(cls, barcode):

        product_id = Barcode.get_product_by_barcode(
            barcode
        )


        if product_id:

            return cls.get_by_id(
                product_id
            )


        return None