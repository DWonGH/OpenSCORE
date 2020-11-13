import json
import sys
import os

from PyQt5.QtWidgets import QStatusBar, QFileDialog, QErrorMessage, QAction, QToolBar, QMessageBox, QInputDialog, QLineEdit, QWidget, QVBoxLayout, QApplication, QMainWindow, QTreeView, QCheckBox, QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import diagnostic_significance

import qtmodern.styles
import qtmodern.windows
import dialogs
from MainWindow import MainWindow


if __name__ == '__main__':
    mod_window = False
    if mod_window:
        app = QApplication(sys.argv)
        qtmodern.styles.light(app)
        mw = qtmodern.windows.ModernWindow(MainWindow())
        mw.show()
        sys.exit(app.exec_())
    else:
        app = QApplication(sys.argv)
        demo = MainWindow()
        demo.show()
        sys.exit(app.exec_())