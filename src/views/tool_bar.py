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

        self.bt_previous_recording = QAction("&Previous", self)
        # self.bt_previous_recording.triggered.connect(self.hdl_previous_recording)
        self.addAction(self.bt_previous_recording)

        self.bt_next_recording = QAction("&Next", self)
        # self.bt_next_recording.triggered.connect(self.hdl_next_recording)
        self.addAction(self.bt_next_recording)

        self.bt_open_in_edfbrowser = QAction("&Open in EDFBrowser", self)
        # self.bt_open_in_edfbrowser.triggered.connect(self.hdl_open_in_edfbrowser)
        self.addAction(self.bt_open_in_edfbrowser)

        self.start_analysis = QAction("&Start Analysis", self)
        # self.next_recording.triggered.connect(self.eeg_graph.start_analysis)
        self.addAction(self.start_analysis)

        self.stop_analysis = QAction("&Stop Analysis", self)
        # self.next_recording.triggered.connect(self.eeg_graph.stop_analysis)
        self.addAction(self.stop_analysis)