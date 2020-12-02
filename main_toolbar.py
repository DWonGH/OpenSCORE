from PyQt5.QtWidgets import QToolBar, QAction


class MainToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.bt_previous_recording = QAction("&Previous", self)
        # self.next_recording.triggered.connect(self.eeg_graph.decrease_volts_scale)
        self.addAction(self.bt_previous_recording)

        self.next_recording = QAction("&Next", self)
        #self.next_recording.triggered.connect(self.eeg_graph.decrease_volts_scale)
        self.addAction(self.next_recording)

        self.start_analysis = QAction("&Start Analysis", self)
        # self.next_recording.triggered.connect(self.eeg_graph.start_analysis)
        self.addAction(self.start_analysis)

        self.stop_analysis = QAction("&Stop Analysis", self)
        # self.next_recording.triggered.connect(self.eeg_graph.stop_analysis)
        self.addAction(self.stop_analysis)

    def hdl_next_recording(self):
        # First check if the user has saved
        # If the user hasnt saved then show pop up dialog warning about lost work
        # Change the main windows current index to + 1
        # Call the main windows load recording
        pass