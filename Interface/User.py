from PyQt6.QtWidgets import *

from Model.User import User


class UserDialog(QDialog):

    def __init__(self, user=None):

        super().__init__()

        self.user = user

        self.setWindowTitle(
            "Edit User" if user else "Create User"
        )

        self.setFixedSize(
            350,
            250
        )

        self.setup_ui()


        if self.user:
            self.load_user()



    def setup_ui(self):

        layout = QVBoxLayout(self)


        # Username

        layout.addWidget(
            QLabel("Username")
        )


        self.username = QLineEdit()


        layout.addWidget(
            self.username
        )


        # Password

        layout.addWidget(
            QLabel("Password")
        )


        self.password = QLineEdit()


        self.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )


        layout.addWidget(
            self.password
        )


        # Role

        layout.addWidget(
            QLabel("Role")
        )


        self.role = QComboBox()


        self.role.addItems([
            "admin",
            "caissier"
        ])


        layout.addWidget(
            self.role
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



    def load_user(self):

        self.username.setText(
            self.user.username
        )


        self.role.setCurrentText(
            self.user.role
        )


        self.password.setText(
            self.user.password
        )



    def save(self):

        username = self.username.text().strip()

        password = self.password.text()


        if not username or not password:

            QMessageBox.warning(
                self,
                "Error",
                "Username and password required"
            )

            return



        if self.user is None:


            self.user = User(
                username=username,
                password=password,
                role=self.role.currentText()
            )


            self.user.create()



        else:


            self.user.username = username

            self.user.password = password

            self.user.role = (
                self.role.currentText()
            )


            self.user.update()



        self.accept()
class UserWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.selected_user_id = None

        self.setWindowTitle(
            "Users"
        )

        self.resize(
            800,
            500
        )

        self.setup_ui()

        self.load_users()



    def setup_ui(self):

        layout = QVBoxLayout(self)


        layout.addWidget(
            QLabel("Users")
        )


        # ---------------- SEARCH ----------------

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search username..."
        )

        self.search.textChanged.connect(
            self.search_users
        )


        layout.addWidget(
            self.search
        )


        # ---------------- TABLE ----------------


        self.user_table = QTableWidget()

        self.user_table.setColumnCount(4)


        self.user_table.setHorizontalHeaderLabels([
            "ID",
            "Username",
            "Role",
            "Created At"
        ])


        self.user_table.cellClicked.connect(
            self.user_selected
        )


        layout.addWidget(
            self.user_table
        )


        # ---------------- BUTTONS ----------------


        buttons = QHBoxLayout()


        self.create_button = QPushButton(
            "Create"
        )

        self.edit_button = QPushButton(
            "Edit"
        )

        self.delete_button = QPushButton(
            "Delete"
        )


        self.create_button.clicked.connect(
            self.create_user
        )


        self.edit_button.clicked.connect(
            self.edit_user
        )


        self.delete_button.clicked.connect(
            self.delete_user
        )


        buttons.addWidget(
            self.create_button
        )


        buttons.addWidget(
            self.edit_button
        )


        buttons.addWidget(
            self.delete_button
        )


        layout.addLayout(
            buttons
        )



    # ----------------------------------------
    # Load users
    # ----------------------------------------

    def load_users(self):

        users = User.get_all()


        self.fill_table(
            users
        )



    def fill_table(self, users):

        self.user_table.setRowCount(
            len(users)
        )


        for row, user in enumerate(users):

            values = [
                user.id,
                user.username,
                user.role,
                user.created_at
            ]


            for col, value in enumerate(values):

                self.user_table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )



    # ----------------------------------------
    # Search
    # ----------------------------------------

    def search_users(self):

        text = self.search.text().lower()


        users = User.get_all()


        filtered = [
            u for u in users
            if text in u.username.lower()
        ]


        self.fill_table(
            filtered
        )



    # ----------------------------------------
    # Select
    # ----------------------------------------

    def user_selected(self,row,column):

        self.selected_user_id = int(
            self.user_table.item(row,0).text()
        )



    # ----------------------------------------
    # Actions
    # ----------------------------------------

    def create_user(self):

        dialog = UserDialog()


        if dialog.exec():

            self.load_users()


    def edit_user(self):

        if self.selected_user_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Select a user first"
            )

            return


        user = User.get_by_id(
            self.selected_user_id
        )


        dialog = UserDialog(
            user
        )


        if dialog.exec():

            self.load_users()



    def delete_user(self):

        if self.selected_user_id is None:

            QMessageBox.warning(
                self,
                "Error",
                "Select a user first"
            )

            return


        user = User.get_by_id(
            self.selected_user_id
        )


        reply = QMessageBox.question(
            self,
            "Delete User",
            f"Delete {user.username}?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )


        if reply == QMessageBox.StandardButton.Yes:

            user.delete()


            self.selected_user_id = None


            self.load_users()