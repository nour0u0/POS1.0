import sys

from PyQt6.QtWidgets import QApplication

from Interface.Login import LoginWindow


def main():

    app = QApplication(sys.argv)

    login = LoginWindow()

    login.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()