import json
import os

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStatusBar, QPushButton

from modules.main_tab_view import MainTabWidget
from modules.main_toolbar import MainToolBar
from modules.menu_bar import MainMenuBar
from modules.ui_state import UiModel


class MainWindow(QMainWindow):

    def __init__(self):
        """
        Sets up the main program window and widgets
        """
        super().__init__()

        self.ui_model = UiModel(self)

        self.setWindowTitle('OpenSCORE')
        self.resize(558, 500)

        self.menu = MainMenuBar(self, self.ui_model)
        self.setMenuBar(self.menu)

        self.toolbar = MainToolBar(self, self.ui_model)
        self.addToolBar(self.toolbar)

        self.main_tab_view = MainTabWidget(self)  # The main scoring section

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.main_tab_view)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def update(self):
        self.clear_tabview()
        self.toolbar.lbl_current_eeg_name.setText(self.ui_model.current_output_filename)
        if os.path.exists(self.ui_model.report_path):
            with open(self.ui_model.report_path, 'r') as f:
                report = json.load(f)
                self.main_tab_view.set_fields(report)
        elif os.path.exists(self.ui_model.current_txt_path):
            with open(self.ui_model.current_txt_path, 'r') as f:
                self.main_tab_view.patient_details_tab.patient_info_tab.txe_history.setText(f.read())
        self.main_tab_view.clinical_comments.txe_interpreter_name.setText(self.ui_model.interpreter_name)

    def clear_tabview(self):
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().deleteLater()
        del self.main_tab_view
        self.main_tab_view = MainTabWidget(self)
        self.main_layout.addWidget(self.main_tab_view)


