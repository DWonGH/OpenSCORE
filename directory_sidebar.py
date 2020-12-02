from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QTreeView, QFileSystemModel


class FileViewTree(QTreeView):
    def __init__(self, parent):
        super().__init__()

        self.setMinimumWidth(250)

        self.main_data_directory = f"E:\\computer_science\\living_lab\\2020TEETACSI\\Data\\tueg-tools\\data\\v2.0.0\\edf"
        self.current_working_directory = None
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.data_directory_index = self.model.index(self.main_data_directory)

        self.setModel(self.model)
        self.setRootIndex(self.data_directory_index)
        self.hideColumn(3)
        self.hideColumn(2)
        self.hideColumn(1)

    def currentChanged(self, current, previous):
        self.current_working_directory = self.currentIndex()
        print(self.current_working_directory.data)
        print(QDir.currentPath())

