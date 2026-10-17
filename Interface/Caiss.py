from PyQt6.QtWidgets import *

from PyQt6.QtCore import *

from Model.Product import Product
from Model.Invoice import Invoice
from Model.InvoiceItems import InvoiceItem
from Model.Barcode import Barcode

class ProductSearchDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.selected_product = None
        self.selected_barcode = None

        self.setWindowTitle("Search Product")
        self.resize(700, 400)

        self.setup_ui()


    def setup_ui(self):

        layout = QVBoxLayout(self)


        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search by barcode or name"
        )

        self.search.textChanged.connect(
            self.search_product
        )


        layout.addWidget(
            self.search
        )


        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Name",
            "Designation",
            "Barcode"
        ])

        self.table.cellDoubleClicked.connect(
            self.select_product
        )


        layout.addWidget(
            self.table
        )



    def search_product(self, text):

        text = text.strip()

        if not text:
            self.table.setRowCount(0)
            return


        products = []


        # Try barcode first

        product = Product.get_by_barcode(
            text
        )


        if product:

            products.append(product)


        else:

            # Search by name

            products = Product.search(
                name=text
            )


        self.table.setRowCount(
            len(products)
        )


        for row, product in enumerate(products):

            barcode = self.get_product_barcode(
                product.id
            )


            values = [
                product.id,
                product.name,
                product.designation or "",
                barcode
            ]


            for col, value in enumerate(values):

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )



    def get_product_barcode(self, product_id):

        barcodes = Barcode.get_by_product(
            product_id
        )


        if barcodes:

            return barcodes[0].barcode


        return "None"



    def select_product(self, row, column):

        product_id = int(
            self.table.item(row,0).text()
        )


        self.selected_product = Product.get_by_id(
            product_id
        )


        self.selected_barcode = self.table.item(
            row,
            3
        ).text()


        self.accept()
class CaissierWidget(QWidget):

    def __init__(self, user):

        super().__init__()

        self.user = user

        self.current_invoice_id = None
        self.current_caisse = 1
        self.cart_items = []
        self.caisse_carts = {
            1: [],
            2: [],
            3: []
        }
        self.viewing_old_invoice = False
        self.setWindowTitle(
            "OVA POS - Caisse"
        )

        self.resize(
            1200,
            800
        )

        self.setup_ui()



    def setup_ui(self):

        main = QVBoxLayout(self)


        # ================= TOP =================


        top = QHBoxLayout()


        left_box = QGroupBox(
            "Invoice"
        )


        left_layout = QVBoxLayout()


        buttons = QHBoxLayout()


        self.current_caisse = 1

        self.caisse_buttons = []

        for i in range(1, 4):

            button = QPushButton(f"Caisse {i}")

            button.clicked.connect(
                lambda checked=False, caisse=i: self.select_caisse(caisse)
            )

            self.caisse_buttons.append(button)

            buttons.addWidget(button)





        self.barcode = QLineEdit()

        self.barcode.setPlaceholderText(
            "Scan barcode..."
        )


        received_layout = QHBoxLayout()


        received_layout.addWidget(
            QLabel("Received")
        )


        self.received = QLineEdit()


        received_layout.addWidget(
            self.received
        )



        return_layout = QHBoxLayout()


        return_layout.addWidget(
            QLabel("Return")
        )


        self.return_label = QLabel(
            "0.000"
        )


        return_layout.addWidget(
            self.return_label
        )


        left_layout.addLayout(
            buttons
        )


        left_layout.addWidget(
            self.barcode
        )


        left_layout.addLayout(
            received_layout
        )


        left_layout.addLayout(
            return_layout
        )


        left_box.setLayout(
            left_layout
        )


        top.addWidget(
            left_box,
            3
        )


        # TOTAL

        self.total_label = QLabel(
            "0.000"
        )


        self.total_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        top.addWidget(
            self.total_label,
            1
        )


        main.addLayout(
            top
        )


        # ================= CART =================

        self.cart_table = QTableWidget()


        self.cart_table.setColumnCount(
            5
        )


        self.cart_table.setHorizontalHeaderLabels([
            "Product",
            "Quantity",
            "Price",
            "Total",
            "Barcode"
        ])


        # Stretch columns to fill available space
        header = self.cart_table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )


        # Prevent editing cells
        self.cart_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )


        # Select whole row
        self.cart_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )


        # Allow only one row selection
        self.cart_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )


        # Disable changing column/row size
        header.setSectionsMovable(
            False
        )

        header.setSectionsClickable(
            False
        )


        self.cart_table.verticalHeader().setSectionsClickable(
            False
        )


        main.addWidget(
            self.cart_table
        )
        # ================= BOTTOM =================


        bottom = QHBoxLayout()
        self.validate_btn = QPushButton(
            "Validate"
        )

        self.delete_btn = QPushButton(
            "Delete"
        )

        self.search_btn = QPushButton(
            "Search"
        )


        self.multiply_btn = QPushButton(
            "Multiply"
        )


        self.quantity = QLineEdit()

        self.quantity.setPlaceholderText(
            "Qty"
        )


        self.auto_print = QCheckBox(
            "Auto Print"
        )


        self.print_btn = QPushButton(
            "Print"
        )


        bottom.addWidget(
            self.delete_btn
        )


        bottom.addWidget(
            self.search_btn
        )


        bottom.addWidget(
            self.multiply_btn
        )


        bottom.addWidget(
            self.quantity
        )


        bottom.addStretch()


        bottom.addWidget(
            self.auto_print
        )


        bottom.addWidget(
            self.print_btn
        )
        bottom.addWidget(
        self.validate_btn 
        )
        main.addLayout(
            bottom
        )




        self.setFocusPolicy(
                Qt.FocusPolicy.StrongFocus
            )
        self.cart_table.installEventFilter(self)

        self.setFocusPolicy(
        Qt.FocusPolicy.StrongFocus
        )


        self.barcode.returnPressed.connect(
            self.barcode_entered
        )


        self.received.textChanged.connect(
            self.calculate_return
        )


        self.delete_btn.clicked.connect(
            self.delete_cart_item
        )
        self.validate_btn.clicked.connect(
            self.create_invoice
        )
        self.multiply_btn.clicked.connect(
            self.multiply_item
        )
        self.search_btn.clicked.connect(
            self.search_product
        )
        self.quantity.returnPressed.connect(
            self.apply_multiply
        )

        self.apply_style()
        self.update_caisse_buttons()
    def barcode_entered(self):

        if self.viewing_old_invoice:

            QMessageBox.warning(
                self,
                "Old Invoice",
                "You cannot add products while viewing an old invoice. Create a new invoice first."
            )

            self.barcode.clear()
            return


        barcode = self.barcode.text().strip()

        if not barcode:
            return


        product = Product.get_by_barcode(
            barcode
        )


        if product is None:

            QMessageBox.warning(
                self,
                "Error",
                "Product not found"
            )

            return


        self.add_to_cart(
            product,
            barcode
        )


        self.barcode.clear()
    def add_to_cart(self, product, barcode):


        for item in self.cart_items:

            if item["product_id"] == product.id:

                item["qte"] += 1

                self.refresh_cart()

                return



        self.cart_items.append({

            "product_id": product.id,

            "name": product.name,

            "designation": product.designation,

            "selling_price": product.selling_price,

            "cost": product.cost,

            "barcode": barcode,

            "qte": 1
        })


        self.refresh_cart()



    def refresh_cart(self):

        self.cart_table.setRowCount(
            len(self.cart_items)
        )


        total = 0


        for row,item in enumerate(self.cart_items):


            item_total = (
                item["selling_price"]
                *
                item["qte"]
            )


            total += item_total


            values = [
                item["name"],
                item["qte"],
                item["selling_price"],
                item_total,
                item["barcode"]
            ]


            for col,value in enumerate(values):

                self.cart_table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )


        self.total_label.setText(
            f"{total:.3f}"
        )



    def calculate_return(self):

        try:

            received = float(
                self.received.text()
            )

        except:

            received = 0


        total = float(
            self.total_label.text()
        )


        result = received-total


        if result < 0:
            result = 0


        self.return_label.setText(
            f"{result:.3f}"
        )


    def new_invoice(self):

        self.viewing_old_invoice = False

        self.current_invoice_id = None

        self.cart_items.clear()

        self.received.clear()

        self.refresh_cart()

    def delete_cart_item(self):

        row = self.cart_table.currentRow()


        if row >= 0:

            self.cart_items.pop(
                row
            )

            self.refresh_cart()
    def apply_style(self):

        self.setStyleSheet("""

            QWidget {
                background-color: white;
                font-size: 14px;
            }


            QGroupBox {

                border: 1px solid #d0d0d0;
                border-radius: 10px;
                margin-top: 12px;
                padding: 12px;
                font-weight: bold;
                color: #333;
            }


            QGroupBox::title {

                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px;
                color: #1976D2;
            }


            QLabel {

                color: #333;
                font-size: 16px;
            }


            QLineEdit {

                height: 35px;
                border: 1px solid #bdbdbd;
                border-radius: 6px;
                padding-left: 10px;
                background: white;
            }


            QLineEdit:focus {

                border: 2px solid #1976D2;
            }


            QPushButton {

                height: 38px;
                min-width: 90px;
                border-radius: 7px;
                background-color: #1976D2;
                color: white;
                font-weight: bold;
                border: none;
            }


            QPushButton:hover {

                background-color: #1565C0;
            }


            QPushButton:pressed {

                background-color: #0D47A1;
            }


            QTableWidget {

                border: 1px solid #cccccc;
                border-radius: 8px;
                gridline-color: #dddddd;
                background-color: white;
                selection-background-color: #BBDEFB;
                selection-color: black;
            }


            QHeaderView::section {

                background-color: #1976D2;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }


            QCheckBox {

                font-size: 15px;
                color: #333;
                spacing: 8px;
            }


        """)


        # Big total display

        self.total_label.setStyleSheet("""

            QLabel {

                font-size: 45px;
                font-weight: bold;
                color: #1976D2;
                padding: 20px;
                border: 2px solid #1976D2;
                border-radius: 12px;
                background-color: #E3F2FD;
            }

        """)


        # Return amount

        self.return_label.setStyleSheet("""

            QLabel {

                font-size: 22px;
                font-weight: bold;
                color: #388E3C;
            }

        """)


    def previous_invoice(self):

        # No invoice loaded yet
        # Load the latest saved invoice
        if self.current_invoice_id is None:

            invoice = Invoice.get_last()


        else:

            invoice = Invoice.get_previous(
                self.current_invoice_id
            )


        # No previous invoice found
        if invoice is None:

            QMessageBox.information(
                self,
                "Invoice",
                "No previous invoice found"
            )

            return


        self.load_invoice(
            invoice
        )
    def next_invoice(self):

        # No invoice loaded yet
        # Start from the latest invoice
        if self.current_invoice_id is None:

            invoice = Invoice.get_last()


        else:

            invoice = Invoice.get_next(
                self.current_invoice_id
            )


        # No next invoice found
        if invoice is None:

            QMessageBox.information(
                self,
                "Invoice",
                "No next invoice found"
            )

            return


        self.load_invoice(
            invoice
            )
    def create_invoice(self):

        if not self.cart_items:

            QMessageBox.warning(
                self,
                "Error",
                "Cart is empty"
            )

            return

        total = sum(
            item["selling_price"] * item["qte"]
            for item in self.cart_items
        )

        profit = sum(
            (item["selling_price"] - item["cost"]) * item["qte"]
            for item in self.cart_items
        )

        invoice = Invoice(
            total_price=total,
            profit=profit
        )

        invoice.create()

        for item in self.cart_items:

            invoice_item = InvoiceItem(

                invoice_id=invoice.id,

                name=item["name"],
                designation=item["designation"],
                selling_price=item["selling_price"],
                cost=item["cost"],
                qte=item["qte"]

            )

            invoice_item.create()

            # Update product quantity
            product = Product.get_by_barcode(item["barcode"])

            if product:
                product.qte = max(0, product.qte - item["qte"])
                product.update()

        self.current_invoice_id = invoice.id

        QMessageBox.information(
            self,
            "Success",
            f"Invoice #{invoice.id} saved"
        )

        if self.auto_print.isChecked():
            self.print_invoice(invoice.id)

        # Clear current caisse
        self.cart_items.clear()

        self.caisse_carts[self.current_caisse] = []

        self.current_invoice_id = None

        self.received.clear()

        self.calculate_return()

        self.refresh_cart()

        self.barcode.clear()
        self.barcode.setFocus()
    def multiply_item(self):

        row = self.cart_table.currentRow()


        if row < 0:

            QMessageBox.warning(
                self,
                "Error",
                "Select an item first"
            )

            return


        value = self.quantity.text().strip()


        if not value:

            QMessageBox.warning(
                self,
                "Error",
                "Enter a quantity"
            )

            return


        try:

            qty = int(value)


        except ValueError:

            QMessageBox.warning(
                self,
                "Error",
                "Quantity must be a number"
            )

            return



        if qty <= 0:

            QMessageBox.warning(
                self,
                "Error",
                "Quantity must be greater than zero"
            )

            return



        self.cart_items[row]["qte"] = qty


        self.refresh_cart()


        self.quantity.clear()




    def load_invoice(self, invoice):

        self.viewing_old_invoice = True

        self.current_invoice_id = invoice.id

        self.received.setText(
            str(invoice.total_price)
        )

        self.cart_items.clear()


        items = InvoiceItem.get_by_invoice(
            invoice.id
        )


        for item in items:

            self.cart_items.append({

                "product_id": None,

                "name": item.name,

                "designation": item.designation,

                "selling_price": item.selling_price,

                "cost": item.cost,

                "barcode": "",

                "qte": item.qte

            })


        self.refresh_cart()
    def search_product(self):

        dialog = ProductSearchDialog()

        if dialog.exec():

            product = dialog.selected_product

            barcode = dialog.selected_barcode


            if product:

                self.add_to_cart(
                    product,
                    barcode
                )
    def is_text_active(self):

        widget = self.focusWidget()

        return isinstance(
            widget,
            QLineEdit
    )


    def change_selected_quantity(self, delta):

        row = self.cart_table.currentRow()

        if row < 0:
            return


        item = self.cart_items[row]


        item["qte"] += delta


        if item["qte"] <= 0:
            item["qte"] = 1


        self.refresh_cart()
    def keyPressEvent(self, event):

        key = event.key()
        text = event.text()


        # Do nothing if user is typing in a field
        # except global shortcuts
        if self.is_text_active():

            if key not in [
                Qt.Key.Key_F1,
                Qt.Key.Key_F2
            ] and text != "/":

                super().keyPressEvent(event)
                return



        # Minus decrease quantity
        if text == "-":

            self.change_selected_quantity(-1)

            return



        # Plus increase quantity
        if text == "+":

            self.change_selected_quantity(1)

            return



        # Multiply mode
        if text == "*":

            self.quantity.setFocus()

            self.quantity.selectAll()

            return



        # Divide = validate invoice
        if text == "/":

            self.create_invoice()

            return



        # F1 focus barcode scanner
        if key == Qt.Key.Key_F1:

            self.barcode.setFocus()

            self.barcode.selectAll()

            return



        # F2 open search
        if key == Qt.Key.Key_F2:

            self.search_product()

            return



        # Enter in multiply field
        if key == Qt.Key.Key_Return:

            if self.quantity.hasFocus():

                try:
                    multiplier = int(
                        self.quantity.text()
                    )

                except:
                    multiplier = 1


                row = self.cart_table.currentRow()


                if row >= 0:

                    self.cart_items[row]["qte"] *= multiplier

                    self.refresh_cart()


                self.quantity.clear()

                self.barcode.setFocus()

                return



        super().keyPressEvent(event)
    def apply_multiply(self):
        

        self.multiply_item()
        self.quantity.clear()
        
        self.barcode.setFocus()

        self.barcode.selectAll()


    def update_caisse_buttons(self):

        normal_style = """
            QPushButton {
                height:38px;
                min-width:90px;
                border-radius:7px;
                background:#1976D2;
                color:white;
                font-weight:bold;
                border:none;
            }

            QPushButton:hover {
                background:#1565C0;
            }

            QPushButton:pressed {
                background:#0D47A1;
            }
        """

        selected_style = """
            QPushButton {
                height:38px;
                min-width:90px;
                border-radius:7px;
                background:#D32F2F;
                color:white;
                font-weight:bold;
                border:none;
            }

            QPushButton:hover {
                background:#C62828;
            }

            QPushButton:pressed {
                background:#B71C1C;
            }
        """


        for i, button in enumerate(self.caisse_buttons, start=1):

            if i == self.current_caisse:
                button.setStyleSheet(selected_style)
            else:
                button.setStyleSheet(normal_style)
    def select_caisse(self, caisse):

            if caisse == self.current_caisse:
                return

            # Save current working cart
            self.caisse_carts[self.current_caisse] = [
                item.copy()
                for item in self.cart_items
            ]

            # Switch caisse
            self.current_caisse = caisse

            self.update_caisse_buttons()

            # Load selected caisse
            self.cart_items = [
                item.copy()
                for item in self.caisse_carts[caisse]
            ]

            self.received.clear()
            self.calculate_return()

            self.refresh_cart()

            self.barcode.setFocus()
            self.barcode.selectAll()