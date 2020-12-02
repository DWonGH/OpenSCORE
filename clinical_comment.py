from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QTextEdit


class ClinicalComments(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QFormLayout()

        self.lbl_interpreter_name = QLabel("Interpreter name")
        self.txe_interpreter_name = QLineEdit()
        self.layout.addRow(self.lbl_interpreter_name, self.txe_interpreter_name)

        self.lbl_clinical_comments = QLabel("Clinical comments")
        self.txe_clinical_comments = QTextEdit()
        self.layout.addRow(self.lbl_clinical_comments, self.txe_clinical_comments)

        self.setLayout(self.layout)

    def get_details(self):
        clinical_comments = {
            "Interpreter name": self.txe_interpreter_name.text(),
            "Clinical comments": self.txe_clinical_comments.toPlainText()
        }
        return clinical_comments

    def load_details(self, clinical_comments):
        self.txe_interpreter_name = clinical_comments["Interpreter name"]
        self.txe_clinical_comments = clinical_comments["Clinical comments"]

    def get_check_list(self, chlist):
        results = {}
        for i in range(chlist.rowCount()):
            results[chlist.item(i).text()] = chlist.item(i).checkState()
        return results

