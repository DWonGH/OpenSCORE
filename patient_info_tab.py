from PyQt5.QtWidgets import QLineEdit, QFormLayout, QLabel, QWidget, QTextEdit


class PatientInfoTab(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QFormLayout()

        self.layout.addRow(QLabel("Patient details"))

        self.lbl_name = QLabel("Name")
        self.txe_name = QLineEdit()
        self.layout.addRow(self.lbl_name, self.txe_name)

        self.lbl_id = QLabel("Patient ID")
        self.txe_id = QLineEdit()
        self.layout.addRow(self.lbl_id, self.txe_id)

        # TODO: Change to date edit box
        self.lbl_dob = QLabel("Date of Birth")
        self.txe_dob = QLineEdit()
        self.layout.addRow(self.lbl_dob, self.txe_dob)

        self.lbl_address = QLabel("Address")
        self.txe_address = QLineEdit()
        self.layout.addRow(self.lbl_address, self.txe_address)

        self.lbl_medication = QLabel("Medication")
        self.txe_medication = QTextEdit()
        self.layout.addRow(self.lbl_medication, self.txe_medication)

        self.lbl_history = QLabel("Patient History")
        self.txe_history = QTextEdit()
        self.layout.addRow(self.lbl_history, self.txe_history)

        self.setLayout(self.layout)

    def get_details(self):
        patient_info = {
            "Name": self.txe_name.text(),
            "ID": self.txe_id.text(),
            "Date of Birth": self.txe_dob.text(),
            "Address": self.txe_address.text(),
            "Medication": self.txe_medication.toPlainText(),
            "History": self.txe_history.toPlainText()
        }
        return patient_info

    def load_details(self, patient_info):
        print(patient_info)
        self.txe_name.setText(patient_info["Patient info"]["Name"])
        self.txe_id.setText(patient_info["Patient info"]["ID"])
        self.txe_dob.setText(patient_info["Patient info"]["Date of Birth"])
        self.txe_address.setText(patient_info["Patient info"]["Address"])
        self.txe_medication.setText(patient_info["Patient info"]["Medication"])
        self.txe_history.setText(patient_info["Patient info"]["History"])
