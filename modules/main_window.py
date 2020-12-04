import os

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStatusBar
import mne

from modules.main_tab_view import MainTabWidget
from modules.main_toolbar import MainToolBar
from modules.menu_bar import MainMenuBar


class MainWindow(QMainWindow):

    def __init__(self):
        """
        Sets up the main program window and widgets
        """
        super().__init__()

        self.progress_saved = False
        self.report_file_name = ""
        self.report_path = ""
        self.interpreter_name = None
        self.eeg_sequence_list_location = None  # The path to a txt file describing a list of specified input directories
        self.root_output_directory = None  # A directory path to save the mirror directories
        self.eeg_list = []
        self.current_eeg_index = 0
        self.current_eeg_directory = ""
        self.current_edf_filename = ""
        self.current_edf_path = ""
        self.current_txt_filename = ""
        self.current_txt_path = ""

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

    def load_eeg(self):
        """
        :param eeg_path:
        :return:
        """
        self.clear_tabview()
        files = next(os.walk(self.current_eeg_directory))[2]
        if len(files) == 2:
            for f in files:
                if '.edf' in f:
                    self.current_edf_filename = f
                    self.current_edf_path = os.path.join(self.current_eeg_directory, self.current_edf_filename)
                    self.toolbar.lbl_current_eeg_name.setText(self.current_edf_filename.strip('.edf'))
                if '.txt' in f:
                    self.current_txt_filename = f
                    self.current_txt_path = os.path.join(self.current_eeg_directory, self.current_txt_filename)
                    with open(self.current_txt_path, 'r') as f:
                        notes = f.read()
                        self.main_tab_view.patient_details_tab.patient_info_tab.txe_history.setText(notes)
        else:
            print("Was expecting 2 files, 1 edf and 1 txt")
        if self.interpreter_name is not None:
            self.main_tab_view.clinical_comments.txe_interpreter_name.setText(self.interpreter_name)

    def clear_tabview(self):
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().deleteLater()
        del self.main_tab_view
        self.main_tab_view = MainTabWidget(self)
        self.main_layout.addWidget(self.main_tab_view)

    def clear_session(self):
        self.interpreter_name = ""
        self.eeg_sequence_list_location = ""  # The path to a txt file describing a list of specified input directories
        self.root_output_directory = ""  # A directory path to save the mirror directories
        self.eeg_list = []
        self.current_eeg_index = 0
        self.current_eeg_directory = ""
        self.current_edf_filename = ""
        self.current_edf_path = ""
        self.current_txt_filename = ""
        self.current_txt_path = ""
