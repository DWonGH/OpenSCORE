import json

from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QVBoxLayout, QStatusBar, QHBoxLayout

from main_tab import MainTabWidget
from main_toolbar import MainToolBar
from menu_bar import MainMenuBar


class MainWindow(QMainWindow):

    def __init__(self):
        """
        Sets up the main program window and widgets
        """
        super().__init__()

        self.setWindowTitle('OpenSCORE')
        self.resize(558, 500)

        self.menu = MainMenuBar(self)
        self.setMenuBar(self.menu)

        self.toolbar = MainToolBar(self)
        self.addToolBar(self.toolbar)

        self.main_tab_view = MainTabWidget(self)  # The main scoring section

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.main_tab_view)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.eeg_sequence_list_location = None
        self.eeg_sequence_list = []
        self.root_output_directory = None
