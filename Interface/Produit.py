from PyQt6.QtWidgets import *

from Model.Product import Product
import sqlite3
from Model.Barcode import Barcode
from Model.Product import Product



from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)


class BarcodeDialog(QDialog):

    def __init__(self, barcode=None):
        super().__init__()

        self.barcode = barcode

        self.setWindowTitle(
            "Edit Barcode" if barcode else "Create Barcode"
        )

        self.setFixedSize(
            350,
            180
        )

        self.setup_ui()

        if self.barcode:
            self.load_barcode()


    def setup_ui(self):

        layout = QVBoxLayout(self)


        layout.addWidget(
            QLabel("Barcode")
        )


        self.barcode_input = QLineEdit()

        self.barcode_input.setPlaceholderText(
            "Scan or enter barcode"
        )


        layout.addWidget(
            self.barcode_input
        )


        buttons = QHBoxLayout()


        self.save_button = QPushButton(
            "Save"
        )

        self.cancel_button = QPushButton(
            "Cancel"
        )


        self.save_button.clicked.connect(
            self.save
        )

        self.cancel_button.clicked.connect(
            self.reject
        )


        buttons.addWidget(
            self.save_button
        )

        buttons.addWidget(
            self.cancel_button
        )


        layout.addLayout(
            buttons
        )


    def load_barcode(self):

        self.barcode_input.setText(
            self.barcode.barcode
        )


    def save(self):

        value = self.barcode_input.text().strip()


        if not value:

            QMessageBox.warning(
                self,
                "Error",
                "Barcode cannot be empty"
            )

            return


        self.value = value

        self.accept()


class ProductDialog(QDialog):

    def __init__(self, product=None):
        super().__init__()

        self.product = product
        self.selected_barcode_id = None
        self.setWindowTitle(
            "Edit Product" if product else "Create Product"
        )

        self.setFixedSize(
            400,
            450
        )

        self.setup_ui()

        if self.product:
            self.load_product()


    def setup_ui(self):

        layout = QVBoxLayout(self)


        # Name

        layout.addWidget(
            QLabel("Name")
        )

        self.name = QLineEdit()

        layout.addWidget(
            self.name
        )


        # Designation

        layout.addWidget(
            QLabel("Designation")
        )

        self.designation = QLineEdit()

        layout.addWidget(
            self.designation
        )


        # Selling price

        layout.addWidget(
            QLabel("Selling Price")
        )

        self.selling_price = QDoubleSpinBox()

        self.selling_price.setMaximum(
            999999
        )

        self.selling_price.setDecimals(
            2
        )

        layout.addWidget(
            self.selling_price
        )


        # Cost

        layout.addWidget(
            QLabel("Cost")
        )

        self.cost = QDoubleSpinBox()

        self.cost.setMaximum(
            999999
        )

        self.cost.setDecimals(
            2
        )

        layout.addWidget(
            self.cost
        )


        # Quantity

        layout.addWidget(
            QLabel("Quantity")
        )

        self.qte = QSpinBox()

        self.qte.setMaximum(
            999999
        )

        layout.addWidget(
            self.qte
        )


        # Display

        self.displayed = QCheckBox(
            "Displayed"
        )

        self.displayed.setChecked(
            True
        )

        layout.addWidget(
            self.displayed
        )


        # Buttons

        buttons = QHBoxLayout()


        self.save_button = QPushButton(
            "Save"
        )

        self.cancel_button = QPushButton(
            "Cancel"
        )


        self.save_button.clicked.connect(
            self.save
        )

        self.cancel_button.clicked.connect(
            self.reject
        )


        buttons.addWidget(
            self.save_button
        )

        buttons.addWidget(
            self.cancel_button
        )


        layout.addLayout(
            buttons
        )





    def load_product(self):

        self.name.setText(
            self.product.name
        )

        self.designation.setText(
            self.product.designation or ""
        )

        self.selling_price.setValue(
            self.product.selling_price
        )

        self.cost.setValue(
            self.product.cost
        )

        self.qte.setValue(
            self.product.qte
        )

        self.displayed.setChecked(
            bool(self.product.is_displayed)
        )


    def save(self):

        if not self.name.text().strip():

            QMessageBox.warning(
                self,
                "Error",
                "Product name required"
            )

            return


        if self.product is None:

            self.product = Product(
                name=self.name.text(),
                designation=self.designation.text(),
                selling_price=self.selling_price.value(),
                cost=self.cost.value(),
                qte=self.qte.value(),
                is_displayed=1 if self.displayed.isChecked() else 0
            )

            self.product.create()


        else:

            self.product.name = self.name.text()

            self.product.designation = (
                self.designation.text()
            )

            self.product.selling_price = (
                self.selling_price.value()
            )

            self.product.cost = (
                self.cost.value()
            )

            self.product.qte = (
                self.qte.value()
            )

            self.product.is_displayed = (
                1 if self.displayed.isChecked() else 0
            )


            self.product.update()


        self.accept()


class ProductWidget(QWidget):

    DB_PATH = "DB/DataBase.sqlite"

    def __init__(self):
        super().__init__()

        self.selected_product_id = None

        self.setWindowTitle("Products")
        self.resize(1000, 700)

        self.setup_ui()
        self.load_products()

    def setup_ui(self):

        layout = QVBoxLayout(self)


        # ---------------- PRODUCT SEARCH ----------------

        search_layout = QHBoxLayout()


        self.barcode_search = QLineEdit()

        self.barcode_search.setPlaceholderText(
            "Search by barcode"
        )


        self.name_search = QLineEdit()

        self.name_search.setPlaceholderText(
            "Search by name"
        )


        self.designation_search = QLineEdit()

        self.designation_search.setPlaceholderText(
            "Search by designation"
        )


        search_layout.addWidget(
            self.barcode_search
        )

        search_layout.addWidget(
            self.name_search
        )

        search_layout.addWidget(
            self.designation_search
        )


        layout.addLayout(
            search_layout
        )


        self.barcode_search.textChanged.connect(
            self.search_products
        )

        self.name_search.textChanged.connect(
            self.search_products
        )

        self.designation_search.textChanged.connect(
            self.search_products
        )


        # ---------------- PRODUCTS TABLE ----------------

        layout.addWidget(
            QLabel("Products")
        )


        self.product_table = QTableWidget()

        self.product_table.setColumnCount(7)

        self.product_table.setHorizontalHeaderLabels([
            "ID",
            "Name",
            "Designation",
            "Selling Price",
            "Cost",
            "Quantity",
            "Displayed"
        ])


        self.product_table.cellClicked.connect(
            self.product_selected
        )


        layout.addWidget(
            self.product_table
        )


        # ---------------- PRODUCT BUTTONS ----------------

        product_buttons = QHBoxLayout()


        self.create_button = QPushButton(
            "Create"
        )

        self.edit_button = QPushButton(
            "Edit"
        )

        self.delete_button = QPushButton(
            "Delete"
        )

        self.refresh_button = QPushButton(
            "Refresh"
        )

        self.refresh_button.clicked.connect(
            self.refresh_products
        )
        self.create_button.clicked.connect(
            self.create_product
        )

        self.edit_button.clicked.connect(
            self.edit_product
        )

        self.delete_button.clicked.connect(
            self.delete_product
        )


        product_buttons.addWidget(
            self.create_button
        )

        product_buttons.addWidget(
            self.edit_button
        )

        product_buttons.addWidget(
            self.delete_button
        )
        product_buttons.addWidget(
            self.refresh_button
        )

        layout.addLayout(
            product_buttons
        )


        # ---------------- BARCODE TABLE ----------------

        layout.addWidget(
            QLabel("Barcodes")
        )


        self.barcode_table = QTableWidget()


        self.barcode_table.setColumnCount(2)


        self.barcode_table.setHorizontalHeaderLabels([
            "ID",
            "Barcode"
        ])


        self.barcode_table.cellClicked.connect(
            self.barcode_selected
        )


        layout.addWidget(
            self.barcode_table
        )


        # ---------------- BARCODE BUTTONS ----------------

        barcode_buttons = QHBoxLayout()


        self.create_barcode_button = QPushButton(
            "Create Barcode"
        )

        self.edit_barcode_button = QPushButton(
            "Edit Barcode"
        )

        self.delete_barcode_button = QPushButton(
            "Delete Barcode"
        )


        self.create_barcode_button.clicked.connect(
            self.create_barcode
        )

        self.edit_barcode_button.clicked.connect(
            self.edit_barcode
        )

        self.delete_barcode_button.clicked.connect(
            self.delete_barcode
        )


        barcode_buttons.addWidget(
            self.create_barcode_button
        )

        barcode_buttons.addWidget(
            self.edit_barcode_button
        )

        barcode_buttons.addWidget(
            self.delete_barcode_button
        )


        layout.addLayout(
            barcode_buttons
        )  # --------------------------------------------------
    # Products
    # --------------------------------------------------

    def load_products(self):

        products = Product.get_all()

        self.product_table.setRowCount(
            len(products)
        )


        for row, product in enumerate(products):

            values = [
                product.id,
                product.name,
                product.designation,
                product.selling_price,
                product.cost,
                product.qte,
                "Yes" if product.is_displayed else "No"
            ]


            for col, value in enumerate(values):

                self.product_table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )


    def product_selected(self, row, column):

        self.selected_product_id = int(
            self.product_table.item(row,0).text()
        )

        self.load_barcodes(
            self.selected_product_id
        )


    # --------------------------------------------------
    # Barcodes
    # --------------------------------------------------

    def load_barcodes(self, product_id):

        conn = sqlite3.connect(
            self.DB_PATH
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, barcode
            FROM barcodes
            WHERE product_id = ?
        """, (
            product_id,
        ))

        rows = cursor.fetchall()

        conn.close()


        self.barcode_table.setRowCount(
            len(rows)
        )


        for row, data in enumerate(rows):

            self.barcode_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(data[0])
                )
            )

            self.barcode_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    data[1]
                )
            )


    # --------------------------------------------------
    # Actions
    # --------------------------------------------------

    def create_product(self):

        dialog = ProductDialog()

        if dialog.exec():

            self.load_products()

    def edit_product(self):

        if self.selected_product_id:

            product = Product.get_by_id(
                self.selected_product_id
            )

            dialog = ProductDialog(
                product
            )

            if dialog.exec():

                self.load_products()

    def delete_product(self):

        if self.selected_product_id:

            product = Product.get_by_id(
                self.selected_product_id
            )

            product.delete()

            self.selected_product_id = None

            self.load_products()

            self.barcode_table.setRowCount(0)
    def barcode_selected(self, row, column):

        self.selected_barcode_id = int(
        self.barcode_table.item(row,0).text()
        )




    def create_barcode(self):

        if self.selected_product_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Select a product first"
            )

            return


        dialog = BarcodeDialog()


        if dialog.exec():

            barcode = Barcode(
                product_id=self.selected_product_id,
                barcode=dialog.value
            )

            try:
                barcode.create()

            except Exception as e:

                QMessageBox.warning(
                    self,
                    "Error",
                    str(e)
                )

                return


            self.load_barcodes(
                self.selected_product_id
            )
    def edit_barcode(self):

        if self.selected_barcode_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Select a barcode first"
            )

            return


        barcode = Barcode.get_by_id(
            self.selected_barcode_id
        )


        dialog = BarcodeDialog(
            barcode
        )


        if dialog.exec():

            barcode.barcode = dialog.value

            try:
                barcode.update()

            except Exception as e:

                QMessageBox.warning(
                    self,
                    "Error",
                    str(e)
                )

                return


            self.load_barcodes(
                self.selected_product_id
            )
    def delete_barcode(self):

        if self.selected_barcode_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Select a barcode first"
            )

            return


        reply = QMessageBox.question(
            self,
            "Delete Barcode",
            "Are you sure you want to delete this barcode?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )


        if reply != QMessageBox.StandardButton.Yes:
            return


        barcode = Barcode.get_by_id(
            self.selected_barcode_id
        )


        if barcode:

            barcode.delete()


        self.selected_barcode_id = None


        self.load_barcodes(
            self.selected_product_id
            )
    def search_products(self):

        products = Product.search(
            barcode=self.barcode_search.text(),
            name=self.name_search.text(),
            designation=self.designation_search.text()
        )


        self.product_table.setRowCount(
            len(products)
        )


        for row, product in enumerate(products):

            values = [
                product.id,
                product.name,
                product.designation,
                product.selling_price,
                product.cost,
                product.qte,
                "Yes" if product.is_displayed else "No"
            ]


            for col, value in enumerate(values):

                self.product_table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )
    def refresh_products(self):

        self.selected_product_id = None
        self.selected_barcode_id = None

        self.barcode_search.clear()
        self.name_search.clear()
        self.designation_search.clear()

        self.load_products()

        self.barcode_table.setRowCount(0)