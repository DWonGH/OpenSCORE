import json
import os

from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QVBoxLayout, QStatusBar, QHBoxLayout
import mne

from main_tab_view import MainTabWidget
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

        self.progress_saved = False

        self.interpreter_name = None
        self.eeg_sequence_list_location = None  # The path to a txt file describing a list of specified input directories
        self.root_output_directory = None  # A directory path to save the mirror directories

        self.eeg_sequence_list = []  # A list of directory paths
        self.current_eeg_index = 0  # Keep track of which recording we are analyzing
        self.current_eeg_edf = None  # A raw mne object
        self.current_eeg_fname = None  # filename of the current edf
        self.current_eeg_txt = None  # The

    def load_tueg_recording(self, i):
        files = next(os.walk(self.eeg_sequence_list[i]))[2]
        if len(files) == 2:
            for f in files:
                if '.edf' in f:
                    self.current_eeg_fname = f
                if '.txt' in f:
                    self.current_eeg_txt = f
        else:
            # TODO: Add a pop up warning
            print(f"There should only be two files in a TUEG EEG recording. Found {len(files)}")
        edf_path = os.path.join(self.eeg_sequence_list[i], self.current_eeg_fname)
        txt_path = os.path.join(self.eeg_sequence_list[i], self.current_eeg_txt)
        self.current_eeg_edf = mne.io.read_raw_edf(edf_path)
        with open(txt_path, 'r') as f:
            notes = f.read()
            self.main_tab_view.patient_details_tab.patient_info_tab.txe_history.setText(notes)
        if self.interpreter_name is not None:
            self.main_tab_view.clinical_comments.txe_interpreter_name.setText(self.interpreter_name)
        self.current_eeg_index = i

    def reset_score(self):
        """
        Make each box in score empty for fresh report
        :return:
        """
        pass
