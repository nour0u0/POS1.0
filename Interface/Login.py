from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import Qt

from Model.User import User

from Interface.Admin import AdminWindow
from Interface.Caissier import CaissierWidget


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.user = None
        self.main_window = None

        self.setWindowTitle("OVA POS - Login")
        self.setFixedSize(400, 350)

        self.setup_ui()
        self.apply_style()


    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setSpacing(15)
        layout.setContentsMargins(
            40, 30, 40, 30
        )


        # Brand title

        self.brand = QLabel(
            "OVA POS"
        )

        self.brand.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        # Login title

        self.title = QLabel(
            "Login"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        # Inputs

        self.username_input = QLineEdit()

        self.username_input.setPlaceholderText(
            "Username"
        )


        self.password_input = QLineEdit()

        self.password_input.setPlaceholderText(
            "Password"
        )

        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )


        # Button

        self.login_button = QPushButton(
            "Login"
        )

        self.login_button.clicked.connect(
            self.login
        )


        layout.addWidget(
            self.brand
        )

        layout.addWidget(
            self.title
        )

        layout.addSpacing(15)

        layout.addWidget(
            self.username_input
        )

        layout.addWidget(
            self.password_input
        )

        layout.addSpacing(10)

        layout.addWidget(
            self.login_button
        )


        self.setLayout(
            layout
        )


    def apply_style(self):

        self.setStyleSheet("""

            QWidget {
                background-color: white;
                font-family: Arial;
            }


            QLabel#brand {
                color: #1976D2;
                font-size: 32px;
                font-weight: bold;
            }


            QLabel {
                color: #333333;
                font-size: 16px;
            }


            QLineEdit {

                height: 40px;

                border: 1px solid #cccccc;

                border-radius: 8px;

                padding-left: 12px;

                font-size: 15px;

                background-color: #fafafa;
            }


            QLineEdit:focus {

                border: 2px solid #1976D2;

                background-color: white;
            }


            QPushButton {

                height: 42px;

                background-color: #1976D2;

                color: white;

                border-radius: 8px;

                font-size: 16px;

                font-weight: bold;
            }


            QPushButton:hover {

                background-color: #1565C0;
            }


            QPushButton:pressed {

                background-color: #0D47A1;
            }

        """)


        self.brand.setObjectName(
            "brand"
        )


    def login(self):

        username = self.username_input.text().strip()
        password = self.password_input.text()


        if not username or not password:

            QMessageBox.warning(
                self,
                "Error",
                "Enter username and password"
            )

            return


        user = User.authenticate(
            username,
            password
        )


        if user:

            self.user = user

            self.open_interface()

        else:

            QMessageBox.warning(
                self,
                "Login failed",
                "Invalid username or password"
            )


    def open_interface(self):

        if self.user.role == "admin":

            self.main_window = AdminWindow(
                self.user
            )

        elif self.user.role == "caissier":

            self.main_window = CaissierWidget(
                self.user
            )

        else:

            QMessageBox.warning(
                self,
                "Error",
                "Unknown user role"
            )

            return


        self.main_window.show()

        self.close()



if __name__ == "__main__":

    app = QApplication([])

    window = LoginWindow()

    window.show()

    app.exec()