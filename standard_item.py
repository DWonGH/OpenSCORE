from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QCheckBox, QTreeWidget, QTreeWidgetItem
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont, QColor


class StandardItem(QStandardItem):

    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0), checkable=False):
        super().__init__()

        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)
        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)
        self.setCheckable(checkable)