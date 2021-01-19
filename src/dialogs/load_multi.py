import os
from datetime import datetime

from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QDialogButtonBox, \
    QFileDialog


class StartSessionDialog(QDialog):

    def __init__(self, parent=None):
        """
        A pop-up used when the user wants to load a sequence/ list of EEG's to report / analyse
        :param parent:
        """
        super().__init__()

        self.parent = parent

        now = datetime.now()
        now = now.strftime("%d-%m-%Y_%H-%M")

        self.suggested_path = os.path.join(os.getcwd(), 'data', 'analysis_sessions', now)
        self.root_changed = False

        self.setWindowTitle("Load sequence of EEGs")
        self.setMinimumWidth(500)
        self.layout = QFormLayout()

        self.layout.addRow(QLabel("Setup a new EEG analysis session"))

        self.lbl_interpreter_name = QLabel("Interpreter name")
        self.lne_interpreter_name = QLineEdit()
        self.lne_interpreter_name.textChanged.connect(self.hdl_name_changed)
        self.layout.addRow(self.lbl_interpreter_name, self.lne_interpreter_name)

        self.lbl_root_output_directory = QLabel("Root output directory")
        self.hbx_root_output_directory = QHBoxLayout()
        self.lne_root_output_directory = QLineEdit()
        self.lne_root_output_directory.setText(self.suggested_path)
        self.lne_root_output_directory.textEdited.connect(self.hdl_root_focused)
        self.hbx_root_output_directory.addWidget(self.lne_root_output_directory)
        self.btn_root_output_directory = QPushButton("Browse")
        self.btn_root_output_directory.clicked.connect(self.hdl_browse_input_directory)
        self.hbx_root_output_directory.addWidget(self.btn_root_output_directory)
        self.layout.addRow(self.lbl_root_output_directory, self.hbx_root_output_directory)

        self.lbl_specified_paths = QLabel("Specified recordings")
        self.hbx_specified_paths = QHBoxLayout()
        self.lne_specified_paths = QLineEdit()
        self.hbx_specified_paths.addWidget(self.lne_specified_paths)
        self.btn_specified_paths = QPushButton("Browse")
        self.btn_specified_paths.clicked.connect(self.hdl_browse_specified_paths)
        self.hbx_specified_paths.addWidget(self.btn_specified_paths)
        self.layout.addRow(self.lbl_specified_paths, self.hbx_specified_paths)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def hdl_browse_input_directory(self):
        try:
            browse_dir = QFileDialog.getExistingDirectory(self, caption="Select Directory", options=QFileDialog.ShowDirsOnly)
            self.lne_root_output_directory.setText(browse_dir)
        except Exception as e:
            print(f"Exception {e}")

    def hdl_browse_specified_paths(self):
        try:
            browse_txt, _ = QFileDialog.getOpenFileName(self, caption="Select Input Recordings", filter="Text Files (*.txt)")
            self.lne_specified_paths.setText(browse_txt)
        except Exception as e:
            print(f"Exception {e}")

    def hdl_name_changed(self):
        if not self.root_changed:
            suggested_path = f"{self.suggested_path}_{self.lne_interpreter_name.text()}"
            # if self.lne_interpreter_name == "":
            #     self.suggested_path = self.suggested_path[:-1]
            self.lne_root_output_directory.setText(suggested_path)

    def hdl_root_focused(self):
        self.root_changed = True
