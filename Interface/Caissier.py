from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget
)

from Interface.Caiss import CaissierWidget


class CaissierWindow(QWidget):

    def __init__(self, user):
        super().__init__()
        
        self.user = user

        self.setWindowTitle("POS - Caisse")
        self.resize(1200, 800)
        self.cart = []

        self.total = 0

        self.user = user
        self.setup_ui()


    def setup_ui(self):

        main_layout = QVBoxLayout(self)


        # ---------------- TOP BAR ----------------

        top_bar = QHBoxLayout()


        self.caiss_button = QPushButton(
            "Caiss"
        )


        top_bar.addWidget(
            self.caiss_button
        )

        top_bar.addStretch()


        main_layout.addLayout(
            top_bar
        )


        # ---------------- STACK ----------------

        self.stack = QStackedWidget()


        self.caiss_page = CaissierWidget(
            self.user
        )


        self.stack.addWidget(
            self.caiss_page
        )


        main_layout.addWidget(
            self.stack
        )


        # ---------------- CONNECTION ----------------

        self.caiss_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(
                self.caiss_page
            )
        )