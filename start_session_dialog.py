from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QDialogButtonBox, QFileDialog


class StartSessionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Load sequence of EEGs")
        self.setMinimumWidth(500)
        self.layout = QFormLayout()

        self.layout.addRow(QLabel("Setup a new EEG analysis session"))

        self.lbl_interpreter_name = QLabel("Interpreter name")
        self.txe_interpreter_name = QLineEdit()
        self.layout.addRow(self.lbl_interpreter_name, self.txe_interpreter_name)

        self.lbl_root_output_directory = QLabel("Root output directory")
        self.hbx_root_output_directory = QHBoxLayout()
        self.txe_root_output_directory = QLineEdit()
        self.hbx_root_output_directory.addWidget(self.txe_root_output_directory)
        self.btn_root_output_directory = QPushButton("Browse")
        self.btn_root_output_directory.clicked.connect(self.hdl_browse_input_directory)
        self.hbx_root_output_directory.addWidget(self.btn_root_output_directory)
        self.layout.addRow(self.lbl_root_output_directory, self.hbx_root_output_directory)

        self.lbl_specified_paths = QLabel("Specified recordings")
        self.hbx_specified_paths = QHBoxLayout()
        self.txe_specified_paths = QLineEdit()
        self.hbx_specified_paths.addWidget(self.txe_specified_paths)
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
            self.txe_root_output_directory.setText(browse_dir)
        except Exception as e:
            print(f"Exception choosing the input directory {e}")

    def hdl_browse_specified_paths(self):
        try:
            browse_txt, _ = QFileDialog.getOpenFileName(self, caption="Select Input Recordings", filter="Text Files (*.txt)")
            self.txe_specified_paths.setText(browse_txt)
        except Exception as e:
            print(f"Exception choosing the input recordings {e}")