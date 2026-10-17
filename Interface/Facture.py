from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from Model.Invoice import Invoice
from Model.InvoiceItems import InvoiceItem
from Utils.printer import WindowsPrinter

























class PrinterDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.printer = WindowsPrinter()

        self.setWindowTitle(
            "Printer Configuration"
        )

        self.setFixedSize(
            400,
            250
        )

        self.setup_ui()


    def setup_ui(self):

        layout = QVBoxLayout(self)


        layout.addWidget(
            QLabel("Printer")
        )


        self.printer_box = QComboBox()

        self.printer_box.addItems(
            self.printer.get_printers()
        )


        layout.addWidget(
            self.printer_box
        )


        layout.addWidget(
            QLabel("Paper Size")
        )


        self.form_box = QComboBox()

        try:

            forms = self.printer.get_forms()

            self.form_box.addItems(
                forms
            )

        except Exception as e:

            QMessageBox.warning(
                self,
                "Printer Error",
                str(e)
            )


        layout.addWidget(
            self.form_box
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


        # Load previous configuration

        config = self.printer.load_config()


        if config.get("printer"):

            index = self.printer_box.findText(
                config["printer"]
            )

            if index >= 0:
                self.printer_box.setCurrentIndex(
                    index
                )


        if config.get("form"):

            index = self.form_box.findText(
                config["form"]
            )

            if index >= 0:
                self.form_box.setCurrentIndex(
                    index
                )



    def save(self):

        printer = self.printer_box.currentText()

        form = self.form_box.currentText()


        self.printer.set_config(
            printer,
            form
        )


        self.accept()

class InvoiceWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Invoices")
        self.resize(1000, 700)
        self.selected_invoice_id = None
        self.selected_item_id = None
        self.setup_ui()
        self.load_invoices()


    def setup_ui(self):

        layout = QVBoxLayout(self)


        # ---------------- FILTER ----------------

        filter_layout = QHBoxLayout()


        self.start_date = QDateEdit()

        self.start_date.setCalendarPopup(True)

        self.start_date.setDate(
            QDate.currentDate().addMonths(-1)
        )


        self.end_date = QDateEdit()

        self.end_date.setCalendarPopup(True)

        self.end_date.setDate(
            QDate.currentDate()
        )


        self.filter_button = QPushButton(
            "Filter"
        )


        self.filter_button.clicked.connect(
            self.filter_invoices
        )


        filter_layout.addWidget(
            QLabel("From")
        )

        filter_layout.addWidget(
            self.start_date
        )

        filter_layout.addWidget(
            QLabel("To")
        )

        filter_layout.addWidget(
            self.end_date
        )

        filter_layout.addWidget(
            self.filter_button
        )


        layout.addLayout(
            filter_layout
        )


        # ---------------- SEARCH ----------------


        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search invoice..."
        )


        self.search.textChanged.connect(
            self.search_invoice
        )


        layout.addWidget(
            self.search
        )


        # ---------------- INVOICE TABLE ----------------


        layout.addWidget(
            QLabel("Invoices")
        )


        self.invoice_table = QTableWidget()

        self.invoice_table.setColumnCount(4)

        self.invoice_table.setHorizontalHeaderLabels([
            "ID",
            "Date",
            "Total",
            "Profit"
        ])


        self.invoice_table.cellClicked.connect(
            self.invoice_selected
        )


        layout.addWidget(
            self.invoice_table
        )


        # ---------------- INVOICE BUTTONS ----------------


        invoice_buttons = QHBoxLayout()


        self.delete_invoice_button = QPushButton(
            "Delete Invoice"
        )

        self.print_invoice_button = QPushButton(
            "Print Invoice"
        )


        self.delete_invoice_button.clicked.connect(
            self.delete_invoice
        )


        self.print_invoice_button.clicked.connect(
            self.print_invoice
        )


        invoice_buttons.addWidget(
            self.delete_invoice_button
        )

        invoice_buttons.addWidget(
            self.print_invoice_button
        )


        layout.addLayout(
            invoice_buttons
        )


        # ---------------- ITEMS TABLE ----------------


        layout.addWidget(
            QLabel("Invoice Items")
        )


        self.items_table = QTableWidget()

        self.items_table.setColumnCount(6)

        self.items_table.setHorizontalHeaderLabels([
            "ID",
            "Name",
            "Designation",
            "Price",
            "Quantity",
            "Total"
        ])


        self.items_table.cellClicked.connect(
            self.item_selected
        )


        layout.addWidget(
            self.items_table
        )


        # ---------------- ITEM BUTTON ----------------


        self.delete_item_button = QPushButton(
            "Delete Invoice Item"
        )


        self.delete_item_button.clicked.connect(
            self.delete_invoice_item
        )


        layout.addWidget(
            self.delete_item_button
        )


        # ---------------- STATISTICS ----------------


        self.stats_label = QLabel()

        self.stats_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.stats_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #1E88E5;
                background-color: #F5F5F5;
                border: 2px solid #1E88E5;
                border-radius: 8px;
                padding: 12px;
            }
        """)

        layout.addWidget(
            self.stats_label
        )
    def load_invoices(self):

        invoices = Invoice.get_all()

        self.invoice_table.setRowCount(
            len(invoices)
        )

        for row, invoice in enumerate(invoices):

            self.invoice_table.setItem(
                row, 0,
                QTableWidgetItem(str(invoice.id))
            )

            self.invoice_table.setItem(
                row, 1,
                QTableWidgetItem(str(invoice.date))
            )

            self.invoice_table.setItem(
                row, 2,
                QTableWidgetItem(
                    str(invoice.total_price)
                )
            )

            self.invoice_table.setItem(
                row, 3,
                QTableWidgetItem(
                    str(invoice.profit)
                )
            )


    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search_invoice(self, text):

        text = text.lower()

        invoices = Invoice.get_all()

        filtered = [
            i for i in invoices
            if text in str(i.id).lower()
            or text in str(i.date).lower()
        ]


        self.invoice_table.setRowCount(
            len(filtered)
        )


        for row, invoice in enumerate(filtered):

            self.invoice_table.setItem(
                row, 0,
                QTableWidgetItem(str(invoice.id))
            )

            self.invoice_table.setItem(
                row, 1,
                QTableWidgetItem(str(invoice.date))
            )

            self.invoice_table.setItem(
                row, 2,
                QTableWidgetItem(str(invoice.total_price))
            )

            self.invoice_table.setItem(
                row, 3,
                QTableWidgetItem(str(invoice.profit))
            )


    # -------------------------------------------------
    # Invoice selected
    # -------------------------------------------------

    def invoice_selected(self, row, column):

        invoice_id = int(
            self.invoice_table.item(row,0).text()
        )

        self.load_items(invoice_id)


    # -------------------------------------------------
    # Load items
    # -------------------------------------------------

    def load_items(self, invoice_id):

        items = InvoiceItem.get_by_invoice(
            invoice_id
        )


        self.items_table.setRowCount(
            len(items)
        )


        for row, item in enumerate(items):

            total = (
                item.selling_price *
                item.qte
            )


            self.items_table.setItem(
                row,0,
                QTableWidgetItem(item.name)
            )

            self.items_table.setItem(
                row,1,
                QTableWidgetItem(
                    item.designation or ""
                )
            )

            self.items_table.setItem(
                row,2,
                QTableWidgetItem(
                    str(item.selling_price)
                )
            )

            self.items_table.setItem(
                row,3,
                QTableWidgetItem(
                    str(item.qte)
                )
            )

            self.items_table.setItem(
                row,4,
                QTableWidgetItem(
                    str(total)
                )
            )
    def invoice_selected(self,row,column):

        self.selected_invoice_id = int(
            self.invoice_table.item(row,0).text()
        )

        self.load_items(
            self.selected_invoice_id
        )
    def item_selected(self,row,column):

        self.selected_item_id = int(
            self.items_table.item(row,0).text()
        )
    def update_statistics(self, invoices):

        revenue = sum(
            i.total_price for i in invoices
        )


        profit = sum(
            i.profit for i in invoices
        )


        percentage = 0

        if revenue:
            percentage = (
                profit / revenue
            ) * 100


        self.stats_label.setText(
            f"Revenue: {revenue:.2f}   "
            f"Profit: {profit:.2f}   "
            f"Profit %: {percentage:.2f}%"
        )
    def filter_invoices(self):

        start = self.start_date.date().toString(
            "yyyy-MM-dd"
        )

        end = self.end_date.date().toString(
            "yyyy-MM-dd"
        )


        invoices = Invoice.get_by_date_range(
            start,
            end
        )


        self.invoice_table.setRowCount(
            len(invoices)
        )


        for row, invoice in enumerate(invoices):

            self.invoice_table.setItem(
                row,
                0,
                QTableWidgetItem(str(invoice.id))
            )

            self.invoice_table.setItem(
                row,
                1,
                QTableWidgetItem(str(invoice.date))
            )

            self.invoice_table.setItem(
                row,
                2,
                QTableWidgetItem(str(invoice.total_price))
            )

            self.invoice_table.setItem(
                row,
                3,
                QTableWidgetItem(str(invoice.profit))
            )


        self.update_statistics(
            invoices
        )
    def delete_invoice(self):

        if self.selected_invoice_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Select an invoice first"
            )

            return


        reply = QMessageBox.question(
            self,
            "Delete Invoice",
            "Are you sure you want to delete this invoice?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )


        if reply != QMessageBox.StandardButton.Yes:
            return


        invoice = Invoice.get_by_id(
            self.selected_invoice_id
        )


        if invoice:

            invoice.delete()


        self.selected_invoice_id = None


        self.load_invoices()

        self.items_table.setRowCount(0)
    def print_invoice(self):

        if self.selected_invoice_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Select an invoice first"
            )

            return


        dialog = PrinterDialog()


        if dialog.exec():


            printer = WindowsPrinter()


            # Here you create your invoice image
            # PIL Image expected by your printer class

            image = self.create_invoice_image(
                self.selected_invoice_id
            )


            printer.print_image(
                image
            )

    def delete_invoice_item(self):

        if self.selected_item_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Select an invoice item first"
            )

            return


        reply = QMessageBox.question(
            self,
            "Delete Invoice Item",
            "Are you sure you want to delete this item?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )


        if reply != QMessageBox.StandardButton.Yes:
            return


        item = InvoiceItem.get_by_id(
            self.selected_item_id
        )


        if item:

            item.delete()


        self.selected_item_id = None


        # reload items of current invoice

        if self.selected_invoice_id:

            self.load_items(
                self.selected_invoice_id
            )