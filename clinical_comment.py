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
        patient_info = self.patient_info_tab.get_details()
        patient_referral = self.patient_referral_tab.get_details()
        patient_details = {
            "Patient info": patient_info,
            "Patient referral": patient_referral
        }
        return patient_details

    def load_details(self, patient_details):
        """
        Pass the corresponding sub-section of patient details to its tab for loading into the UI fields
        :param patient_details: A dictionary containing both a patient_info sub dict and patient_referral sub dict
        :return: True / False on success
        """
        self.patient_info_tab.load_details(patient_details)

    def get_check_list(self, chlist):
        results = {}
        for i in range(chlist.rowCount()):
            results[chlist.item(i).text()] = chlist.item(i).checkState()
        return results

