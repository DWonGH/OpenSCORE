import sys

from PyQt5.QtWidgets import QStatusBar, QFileDialog, QErrorMessage, QAction, QToolBar, QMessageBox, QInputDialog, QLineEdit, QWidget, QVBoxLayout, QApplication, QMainWindow, QTreeView, QCheckBox, QTreeWidget, QTreeWidgetItem, QPushButton

import qtmodern.styles
import qtmodern.windows
from main_window import MainWindow


if __name__ == '__main__':
    mod_window = False  # Choose if we want styling
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