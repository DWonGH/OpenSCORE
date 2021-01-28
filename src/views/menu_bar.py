from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog, QDialog, QMessageBox


class MainMenuBar(QMenuBar):

    def __init__(self, main_window):

        super().__init__(main_window)

        self.main_window = main_window

        self.dialog = QFileDialog()

        self.file_menu = self.addMenu("&File")

        self.bt_new_report = QAction("&New", self)
        self.bt_new_report.setStatusTip("New report")
        self.file_menu.addAction(self.bt_new_report)

        self.bt_open_file = QAction("&Open", self)
        self.bt_open_file.setStatusTip("Open existing report")
        self.file_menu.addAction(self.bt_open_file)

        self.bt_save_file = QAction("&Save", self)
        self.bt_save_file.setStatusTip("Save to current file")
        self.file_menu.addAction(self.bt_save_file)

        self.bt_save_as_file = QAction("&Save as", self)
        self.bt_save_as_file.setStatusTip("Save to new file")
        self.file_menu.addAction(self.bt_save_as_file)

        self.bt_load_single_eeg = QAction("&Load from EDF", self)
        self.bt_load_single_eeg.setStatusTip("Start a new report linked to an EDF file.")
        self.file_menu.addAction(self.bt_load_single_eeg)

        self.bt_close_window = QAction("&Close", self)
        self.bt_close_window.setStatusTip("Exit OpenScore")
        self.file_menu.addAction(self.bt_close_window)