import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTabWidget

from src.controllers.main_window_controller import MainWindowController


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("OpenSCORE")
    app.setOrganizationName("OpenSCORE")
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    main_window_controller = MainWindowController()
    main_window_controller.view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()