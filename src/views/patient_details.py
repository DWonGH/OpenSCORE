from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QTextEdit, QComboBox


class PatientDetailsWidget(QWidget):

    def __init__(self, parent=None):

        super(QWidget, self).__init__(parent)

        self.layout = QFormLayout()

        self.layout.addRow(QLabel("Patient details"))

        self.lbl_name = QLabel("Name")
        self.lne_name = QLineEdit()
        self.layout.addRow(self.lbl_name, self.lne_name)

        self.lbl_id = QLabel("Patient ID")
        self.lne_id = QLineEdit()
        self.layout.addRow(self.lbl_id, self.lne_id)

        # TODO: Change to date edit box
        self.lbl_dob = QLabel("Date of Birth")
        self.lne_dob = QLineEdit(self)
        self.layout.addRow(self.lbl_dob, self.lne_dob)

        self.txt_gender = ["", "Male", "Female"]
        self.lbl_gender = QLabel("Gender")
        self.cmb_gender = QComboBox()
        self.cmb_gender.addItems(self.txt_gender)
        self.layout.addRow(self.lbl_gender, self.cmb_gender)

        self.txt_handedness = ["", "Right", "Left", "Ambidextrous"]
        self.lbl_handedness = QLabel("Handedness")
        self.cmb_handedness = QComboBox()
        self.cmb_handedness.addItems(self.txt_handedness)
        self.layout.addRow(self.lbl_handedness, self.cmb_handedness)

        self.lbl_address = QLabel("Address")
        self.txe_address = QTextEdit()
        self.txe_address.setMaximumHeight(100)
        self.layout.addRow(self.lbl_address, self.txe_address)

        self.lbl_medication = QLabel("Medication")
        self.txe_medication = QTextEdit()
        self.txe_medication.setMaximumHeight(100)
        self.layout.addRow(self.lbl_medication, self.txe_medication)

        self.lbl_history = QLabel("Patient History")
        self.txe_history = QTextEdit()
        self.layout.addRow(self.lbl_history, self.txe_history)

        self.setLayout(self.layout)

    def to_dict(self):
        data = {
            "Patient name": self.lne_name.text(),
            "Patient ID": self.lne_id.text(),
            "Patient DOB": self.lne_dob.text(),
            "Patient gender": self.cmb_gender.currentText(),
            "Patient handedness": self.cmb_handedness.currentText(),
            "Patient address": self.txe_address.toPlainText(),
            "Patient medication": self.txe_medication.toPlainText(),
            "Patient history": self.txe_history.toPlainText()
        }
        return data

    def update_from_dict(self, data):
        self.lne_name.setText(data['Patient name'])
        self.lne_id.setText(data['Patient ID'])
        self.lne_dob.setText(data['Patient DOB'])
        if data['Patient gender'] is None:
            self.cmb_gender.setCurrentIndex(0)
        else:
            self.cmb_gender.setCurrentIndex(self.txt_gender.index(data['Patient gender']))
        if data['Patient handedness'] is None:
            self.cmb_handedness.setCurrentIndex(0)
        else:
            self.cmb_handedness.setCurrentIndex(self.txt_handedness.index(data['Patient handedness']))
        self.txe_address.setText(data['Patient address'])
        self.txe_medication.setText(data['Patient medication'])
        self.txe_history.setText(data['Patient history'])
