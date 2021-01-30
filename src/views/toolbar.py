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
