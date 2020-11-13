import json
import sys
import os

from PyQt5.QtWidgets import QStatusBar, QFileDialog, QErrorMessage, QAction, QToolBar, QMessageBox, QInputDialog, QLineEdit, QWidget, QVBoxLayout, QApplication, QMainWindow, QTreeView, QCheckBox, QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import diagnostic_significance

import qtmodern.styles
import qtmodern.windows


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('openSCORE')
        app.setStyle("DarkStyle")
        self.resize(500, 300)

        cwd = os.getcwd()
        self.report_dir = os.path.join(cwd, "reports")
        self.report_name = ""
        self.file_name = "report_1"
        if not os.path.exists(self.report_dir):
            os.mkdir(self.report_dir)

        self.model = QStandardItemModel()
        self.root_node = self.model.invisibleRootItem()
        self.root_node.appendRow(diagnostic_significance.get_node())

        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setModel(self.model)
        self.tree_view.expandAll()

        button_action = QAction("&New", self)
        button_action.setStatusTip("New report")
        button_action.triggered.connect(self.hdl_new_report)

        button_action1 = QAction("&Open", self)
        button_action1.setStatusTip("Open existing report")
        button_action1.triggered.connect(self.hdl_open_report)

        button_action2 = QAction("&Save", self)
        button_action2.setStatusTip("Save a file")
        button_action2.triggered.connect(self.hdl_save_report)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)
        file_menu.addAction(button_action1)
        file_menu.addAction(button_action2)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_view)
        self.tree_view.hide()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def hdl_new_report(self):
        self.report_name = self.get_text("New Report", "Enter new report name")
        if self.report_name is not None:
            # TODO: Open a pop up explaining we are going to overwrite the current data
            pass
        self.setWindowTitle(f"openSCORE - {self.report_name}")
        self.tree_view.show()
        if self.root_node is not None:
            for sections in range(self.root_node.rowCount()):
                section = self.root_node.child(sections, 0)
                if section.hasChildren():
                    for features in range(section.rowCount()):
                        feature = section.child(features, 0)
                        if feature.hasChildren():
                            for feature_options in range(feature.rowCount()):
                                feature_option = feature.child(feature_options, 0)
                                feature_option.setData(0, role=Qt.CheckStateRole)

    def hdl_open_report(self):
        # TODO: Parse a JSON file and generate a standardItemModel to load into the QTreeView
        raise NotImplementedError
        #fname = self.open_file_name_dialog()

    def hdl_save_report(self):
        """
        First find out which boxes have been ticked and generate a dict describing the report,
        Then ask the user where they want to save the report.
        :return:
        """
        # Generate report
        report = {}
        if self.root_node is not None:
            for sections in range(self.root_node.rowCount()):
                section = self.root_node.child(sections, 0)
                report[section.data(role=Qt.DisplayRole)] = []
                if section.hasChildren():
                    for features in range(section.rowCount()):
                        feature = section.child(features, 0)
                        report[section.data(role=Qt.DisplayRole)].append({feature.data(role=Qt.DisplayRole): []})
                        if feature.hasChildren():
                            for feature_options in range(feature.rowCount()):
                                feature_option = feature.child(feature_options, 0)
                                report[section.data(role=Qt.DisplayRole)][-1][feature.data(role=Qt.DisplayRole)].append({feature_option.data(role=Qt.DisplayRole): feature_option.data(role=Qt.CheckStateRole)})

        # Write the file
        # TODO: Add check for overwrite
        self.file_name = self.save_file_dialog()
        if self.file_name is not None:
            if '.json' not in self.file_name:
                self.file_name = f"{self.file_name}.json"
            if not os.path.exists(self.file_name):
                try:
                    with open(self.file_name, 'w') as f:
                        json.dump(report, f, indent=2)
                except Exception as e:
                    error_dialog = QErrorMessage()
                    error_dialog.showMessage(f"Could'nt save the file, {e}")

    def save_file_dialog(self):
        """
        File explorer pop up to choose file save locations
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        dialog.setDefaultSuffix('json')
        fileName, _ = dialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", self.report_name,
                                                  "JSON Files (*.json)", options=options)
        if fileName:
            print(fileName)
            return fileName

    def open_file_name_dialog(self):
        """
        File explorer pop up to locate and open a ready made file
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        dialog.setDefaultSuffix('json')
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "JSON Files (*.json)", options=options)
        if fileName:
            print(fileName)
            return fileName

    def get_text(self, title, message):
        text, okPressed = QInputDialog.getText(self, f"{title}", f"{message}", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
            return text




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