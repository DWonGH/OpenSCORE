from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QTextEdit


class ClinicalCommentsWidget(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.layout = QFormLayout()

        self.lbl_interpreter_name = QLabel("Interpreter name")
        self.txe_interpreter_name = QLineEdit()
        self.layout.addRow(self.lbl_interpreter_name, self.txe_interpreter_name)

        self.lbl_clinical_comments = QLabel("Clinical comments")
        self.txe_clinical_comments = QTextEdit()
        self.layout.addRow(self.lbl_clinical_comments, self.txe_clinical_comments)

        self.setLayout(self.layout)

    def to_dict(self):
        data = {
            "Interpreter name": self.txe_interpreter_name.text(),
            "Clinical comments": self.txe_clinical_comments.toPlainText()
        }
        return data

    def update_from_dict(self, data):
        self.txe_interpreter_name.setText(data["Interpreter name"])
        self.txe_clinical_comments.setText(data["Clinical comments"])