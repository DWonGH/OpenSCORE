from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from background_activity import BackgroundActivityTab


class FindingsTab(QWidget):

    def __init__(self, parent):
        """
        Findings is 1 of the 5 main categories in the SCORE standard. Under findings there is a further
        8 sub categories e.g. background activity, interictal findings, Rhythmic or periodic patterns,
        EEG artifacts, ploygraphic channels etc...
        :param parent: MainTabWidget
        """
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.background_activity_tab = BackgroundActivityTab(self)
        # TODO: Sleep & Drowsiness
        # TODO: Interictal findings
        # TODO: Rhythmic or periodic patterns (RPP)
        # TODO: Episodes
        # TODO: Physiologic patters
        # TODO: EEG Artifacts
        # TODO: Polygraphic channels
        # TODO: Trend Analysis
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.background_activity_tab, "Background Activity")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)