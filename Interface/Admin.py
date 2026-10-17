from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget
)

from Interface.Caiss import CaissierWidget
from Interface.Produit import ProductWidget
from Interface.Facture import InvoiceWidget
from Interface.User import UserWidget


class AdminWindow(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle(
            "OVA POS - Admin"
        )

        self.resize(
            1200,
            800
        )

        self.setup_ui()
        self.apply_style()


    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            10, 10, 10, 10
        )

        main_layout.setSpacing(
            10
        )


        # ---------------- TOP BAR ----------------

        top_container = QWidget()

        top_bar = QHBoxLayout(
            top_container
        )

        top_bar.setContentsMargins(
            10, 5, 10, 5
        )


        self.caiss_button = QPushButton(
            "Caiss"
        )

        self.product_button = QPushButton(
            "Products"
        )

        self.invoice_button = QPushButton(
            "Invoices"
        )

        self.user_button = QPushButton(
            "Users"
        )


        top_bar.addWidget(
            self.caiss_button
        )

        top_bar.addWidget(
            self.product_button
        )

        top_bar.addWidget(
            self.invoice_button
        )

        top_bar.addWidget(
            self.user_button
        )


        top_bar.addStretch()


        main_layout.addWidget(
            top_container
        )


        # ---------------- STACK ----------------

        self.stack = QStackedWidget()


        self.caiss_page = CaissierWidget(
            self.user
        )

        self.product_page = ProductWidget()

        self.invoice_page = InvoiceWidget()

        self.user_page = UserWidget()


        self.stack.addWidget(
            self.caiss_page
        )

        self.stack.addWidget(
            self.product_page
        )

        self.stack.addWidget(
            self.invoice_page
        )

        self.stack.addWidget(
            self.user_page
        )


        main_layout.addWidget(
            self.stack
        )


        # ---------------- CONNECTIONS ----------------

        self.caiss_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(
                self.caiss_page
            )
        )

        self.product_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(
                self.product_page
            )
        )

        self.invoice_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(
                self.invoice_page
            )
        )

        self.user_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(
                self.user_page
            )
        )


    def apply_style(self):

        self.setStyleSheet("""

            QWidget {

                background-color:white;

                font-family:Arial;

            }


            QPushButton {

                background-color:#1976D2;

                color:white;

                border:none;

                border-radius:8px;

                padding:10px 25px;

                font-size:15px;

                font-weight:bold;

            }


            QPushButton:hover {

                background-color:#1565C0;

            }


            QPushButton:pressed {

                background-color:#0D47A1;

            }


            QStackedWidget {

                border:1px solid #dddddd;

                border-radius:10px;

                background:white;

            }

        """)


        # top bar styling

        self.caiss_button.setStyleSheet(
            self.button_style()
        )

        self.product_button.setStyleSheet(
            self.button_style()
        )

        self.invoice_button.setStyleSheet(
            self.button_style()
        )

        self.user_button.setStyleSheet(
            self.button_style()
        )


    def button_style(self):

        return """

            QPushButton {

                background:#1976D2;

                color:white;

                border-radius:8px;

                padding:12px 30px;

            }


            QPushButton:hover {

                background:#1565C0;

            }


            QPushButton:pressed {

                background:#0D47A1;

            }

        """