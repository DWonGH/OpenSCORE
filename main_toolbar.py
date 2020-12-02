import os
import subprocess

from PyQt5.QtWidgets import QToolBar, QAction, QLabel


class MainToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.lbl_current_eeg = QLabel("Current EEG: ")
        self.addWidget(self.lbl_current_eeg)

        self.lbl_current_eeg_name = QLabel(self.parent.current_eeg_fname)
        self.lbl_current_eeg_name.setMinimumWidth(110)
        self.addWidget(self.lbl_current_eeg_name)

        self.bt_previous_recording = QAction("&Previous", self)
        self.bt_previous_recording.triggered.connect(self.hdl_previous_recording)
        self.addAction(self.bt_previous_recording)

        self.bt_next_recording = QAction("&Next", self)
        self.bt_next_recording.triggered.connect(self.hdl_next_recording)
        self.addAction(self.bt_next_recording)

        self.bt_open_in_edfbrowser = QAction("&Open in EDFBrowser", self)
        self.bt_open_in_edfbrowser.triggered.connect(self.hdl_open_in_edfbrowser)
        self.addAction(self.bt_open_in_edfbrowser)

        self.start_analysis = QAction("&Start Analysis", self)
        # self.next_recording.triggered.connect(self.eeg_graph.start_analysis)
        self.addAction(self.start_analysis)

        self.stop_analysis = QAction("&Stop Analysis", self)
        # self.next_recording.triggered.connect(self.eeg_graph.stop_analysis)
        self.addAction(self.stop_analysis)

    def hdl_next_recording(self):
        # First check if the user has saved
        # Then check if its the last in the list
        # If the user hasnt saved then show pop up dialog warning about lost work
        # If its the last in the list show a pop up
        # Change the main windows current index to + 1
        # Call the main windows load recording
        if self.parent.progress_saved is False:
            print("you should have saved your progress, we lost it all now")
        if self.parent.current_eeg_index < len(self.parent.eeg_sequence_list)-1:
            print("Moving to next eeg")
            self.parent.current_eeg_index += 1
            self.parent.load_eeg_sequence()
        else:
            print("Thats the last eeg in the list")

    def hdl_previous_recording(self):
        # First check if the user has saved
        # Then check if its the last in the list
        # If the user hasnt saved then show pop up dialog warning about lost work
        # If its the last in the list show a pop up
        # Change the main windows current index to + 1
        # Call the main windows load recording
        if self.parent.progress_saved is False:
            print("you should have saved your progress, we lost it all now")
        if self.parent.current_eeg_index > 0:
            print("Moving to previous eeg")
            self.parent.current_eeg_index -= 1
            self.parent.load_eeg_sequence()
        else:
            print("Thats the last eeg in the list")

    def hdl_open_in_edfbrowser(self):
        # C:\Program Files\EDFbrowser\edfbrowser.exe
        edfbrowser_path = os.path.join('C:\\Program Files\\EDFbrowser\\edfbrowser.exe')
        try:
            edf_path = os.path.join(self.parent.eeg_sequence_list[self.parent.current_eeg_index], self.parent.current_eeg_fname)
            if os.path.exists(edf_path):
                subprocess.Popen([edfbrowser_path, edf_path])
        except Exception as e:
            print(e)