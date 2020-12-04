import json

from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog, QDialog, QMessageBox

from modules.start_session_dialog import StartSessionDialog
import modules.standard_dialogs as dlg


class MainMenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.file_menu = self.addMenu("&File")

        self.bt_new_report = QAction("&New", self)
        self.bt_new_report.setStatusTip("New report")
        self.bt_new_report.triggered.connect(self.hdl_new_report)
        self.file_menu.addAction(self.bt_new_report)

        self.bt_open_file = QAction("&Open", self)
        self.bt_open_file.setStatusTip("Open existing report")
        self.bt_open_file.triggered.connect(self.hdl_open_report)
        self.file_menu.addAction(self.bt_open_file)

        self.bt_save_file = QAction("&Save", self)
        self.bt_save_file.setStatusTip("Save to current file")
        #self.bt_save_file.triggered.connect(self.hdl_save_report)
        self.file_menu.addAction(self.bt_save_file)

        self.bt_save_file = QAction("&Save as", self)
        self.bt_save_file.setStatusTip("Save to new file")
        self.bt_save_file.triggered.connect(self.hdl_save_report)
        self.file_menu.addAction(self.bt_save_file)

        self.bt_load_single_eeg = QAction("&Load EEG", self)
        self.bt_load_single_eeg.setStatusTip("Load a directory containing an EDF (and txt file)")
        self.bt_load_single_eeg.triggered.connect(self.hdl_load_edf_directory)
        self.file_menu.addAction(self.bt_load_single_eeg)

        self.bt_eeg_sequence = QAction("&Load EEG sequence", self)
        self.bt_eeg_sequence.setStatusTip("Load a set of paths to directories containing EDF's")
        self.bt_eeg_sequence.triggered.connect(self.hdl_new_session)
        self.file_menu.addAction(self.bt_eeg_sequence)

        self.bt_close_window = QAction("&Close", self)
        self.bt_close_window.setStatusTip("Exit OpenScore")
        # bt_close_window.triggered.connect(self.close())
        self.file_menu.addAction(self.bt_close_window)

    def hdl_new_report(self):
        """
        Clears the viewer and parameters
        :return:
        """
        result = dlg.confirmation_dialog("Save", "Unsaved progress will be lost, do you want to continue?", QMessageBox.Warning)
        if result == 1024:
            self.parent.clear_tabview()
            self.parent.clear_session()
            self.parent.toolbar.lbl_current_eeg_name.setText("")

    def hdl_save_report(self):
        """
        Save the current score report to a json file
        :return:
        """
        try:
            dialog = QFileDialog()
            dialog.setDefaultSuffix('json')
            save_file, _ = dialog.getSaveFileName(caption="Save Report", filter="JSON Files (*.json)")
            if save_file:
                score = self.parent.main_tab_view.get_fields()
                print(score)
                with open(save_file, 'w') as f:
                    json.dump(score, f, indent=4)
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Warning, e)
            print(e)

    def hdl_open_report(self):
        """
        Loads a json report from file and populates the input fields with the information
        :return:
        """
        try:
            dialog = QFileDialog()
            dialog.setDefaultSuffix('json')
            open_file, _ = dialog.getOpenFileName(caption="Open SCORE Report", filter="JSON Files (*.json)")
            if open_file:
                with open(open_file, 'r') as f:
                    report = json.load(f)
                    self.parent.main_tab_view.set_fields(report)
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Warning, e)
            print(f"Exception {e}")

    def hdl_load_edf_directory(self):
        """
        Ask the user to find a directory where an EDF is located. If the directory contains
        a txt file then it will try and load information from that into the score report
        :return:
        """
        try:
            browse_dir = QFileDialog.getExistingDirectory(self, caption="Select Directory", options=QFileDialog.ShowDirsOnly)
            if browse_dir:
                self.parent.current_eeg_directory = browse_dir
                self.parent.load_eeg()
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Warning, e)
            print(f"Exception choosing the input directory {e}")

    def hdl_new_session(self):
        """
        Prepares a user to analyze multiple EEG recordings. The user must specify a set of paths
        in a txt file to each of the directories containing the required EDFs. The user
        will then be able to move between the files using the "previous" and "next" buttons
        :return:
        """
        try:
            dialog = StartSessionDialog(self)
            if dialog.exec_():
                self.parent.interpreter_name = dialog.txe_interpreter_name.text()
                self.parent.eeg_sequence_list_location = dialog.txe_specified_paths.text()
                self.parent.root_output_directory = dialog.txe_root_output_directory.text()
                with open(self.parent.eeg_sequence_list_location, 'r') as f:
                    self.parent.eeg_list = f.read().splitlines()
                self.parent.current_eeg_directory = self.parent.eeg_list[0]
                self.parent.load_eeg()
            else:
                print("It didnt work :(")
        except Exception as e:
            result = dlg.message_dialog("Exception", "We ran into an error!", QMessageBox.Critical, e)
            print(f"Exception starting a new analysis session {e}")





