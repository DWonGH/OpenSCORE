import json
import sys

from PyQt5.QtWidgets import QTreeWidgetItemIterator, QWidget, QVBoxLayout, QApplication, QMainWindow, QTreeView, QCheckBox, QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import diagnostic_significance


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('openSCORE')
        app.setStyle("plastique")
        self.resize(500, 700)

        self.model = QStandardItemModel()
        self.root_node = self.model.invisibleRootItem()
        self.root_node.appendRow(diagnostic_significance.get_node())

        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setModel(self.model)

        bt_save_report = QPushButton()
        bt_save_report.setText("Save report")
        bt_save_report.clicked.connect(self.hdl_save_report)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_view)
        layout.addWidget(bt_save_report)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def hdl_save_report(self):
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
        print(report)
        with open('report.json', 'w') as f:
            json.dump(report, f, indent=2)

app = QApplication(sys.argv)
demo = MainWindow()
demo.show()
sys.exit(app.exec_())