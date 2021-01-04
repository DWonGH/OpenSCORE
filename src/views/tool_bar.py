from PyQt5.QtWidgets import QToolBar, QAction, QLabel, QMessageBox


class MainToolBar(QToolBar):

    def __init__(self, main_window=None):
        """
        Options for navigating a list of recordings/ reports and opening the corresponding EDF files in EDFBrowser
        :param main_window: MainWindow
        :param ui_model: Manges the paths
        """
        super().__init__()

        self.main_window = main_window

        self.lbl_current_eeg = QLabel("Current EEG: ")
        self.addWidget(self.lbl_current_eeg)

        self.lbl_current_eeg_name = QLabel("")
        self.lbl_current_eeg_name.setMinimumWidth(110)
        self.addWidget(self.lbl_current_eeg_name)

        self.btn_open_in_edfbrowser = QAction("&Open in EDFBrowser", self)
        self.addAction(self.btn_open_in_edfbrowser)

        self.btn_previous_recording = QAction("&Previous", self)
        self.addAction(self.btn_previous_recording)

        self.btn_next_recording = QAction("&Next", self)
        self.addAction(self.btn_next_recording)

        # self.btn_start_analysis = QAction("&Start Analysis", self)
        # self.addAction(self.btn_start_analysis)
        #
        # self.btn_stop_analysis = QAction("&Stop Analysis", self)
        # self.addAction(self.btn_stop_analysis)
        #
        # self.btn_eye_tracker_manager = QAction("&Calibrate Tobii")
        # self.addAction(self.btn_eye_tracker_manager)