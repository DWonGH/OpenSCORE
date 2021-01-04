from PyQt5.QtWidgets import QToolBar, QAction, QLabel, QMessageBox


class TobiiToolBar(QToolBar):

    def __init__(self, main_window=None):
        super().__init__()

        self.main_window = main_window

        self.lbl_toolbar_label = QLabel("Eye Tracker ")
        self.addWidget(self.lbl_toolbar_label)

        self.btn_start_analysis = QAction("&Record Gaze", self)
        self.addAction(self.btn_start_analysis)

        self.btn_stop_analysis = QAction("&Stop Gaze", self)
        self.addAction(self.btn_stop_analysis)

        self.btn_eye_tracker_manager = QAction("&Calibrate Tracker")
        self.addAction(self.btn_eye_tracker_manager)