from PyQt5.QtWidgets import QToolBar, QAction


class MainToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.bt_open_selected = QAction("&Open Selected", self)
        self.bt_open_selected.triggered.connect(self.hdl_open_selected)
        self.addAction(self.bt_open_selected)

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

    def hdl_open_selected(self):
        print(self.parent.file_view_tree.data_directory)