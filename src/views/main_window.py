from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStatusBar, QTabWidget

from src.views.menu_bar import MainMenuBar
from src.views.toolbar import MainToolBar


class MainWindow(QMainWindow):

    def __init__(self, model=None, controller=None):
        """
        Sets up the main program window and widgets
        """
        super().__init__()

        self.model = model
        self.controller = controller

        self.setWindowTitle('OpenSCORE')
        self.resize(558, 500)

        self.menu = MainMenuBar(self)
        self.setMenuBar(self.menu)

        self.toolbar = MainToolBar()
        self.addToolBar(self.toolbar)

        self.main_layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.main_layout.addWidget(self.tabs)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)