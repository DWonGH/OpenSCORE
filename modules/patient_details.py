from PyQt5.QtWidgets import QWidget, QTabWidget,QVBoxLayout

from modules.patient_info_tab import PatientInfoTab
from modules.patient_referral_tab import PatientReferralTab


class PatientDetailTab(QWidget):

    def __init__(self, parent):
        """
        A top-level tab containing sub patient info tabs
        :param parent:
        """
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.patient_info_tab = PatientInfoTab(self)
        self.patient_referral_tab = PatientReferralTab(self)
        self.tabs.addTab(self.patient_info_tab, "Patient Info")
        self.tabs.addTab(self.patient_referral_tab, "Patient Referral")
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def get_fields(self):
        patient_info = self.patient_info_tab.get_fields()
        patient_referral = self.patient_referral_tab.get_fields()
        patient_details = {
            "Patient info": patient_info,
            "Patient referral": patient_referral
        }
        return patient_details

    def set_fields(self, patient_details):
        """
        Pass the corresponding sub-section of patient details to its tab for loading into the UI fields
        :param patient_details: A dictionary containing both a patient_info sub dict and patient_referral sub dict
        :return: True / False on success
        """
        self.patient_info_tab.set_fields(patient_details)
        self.patient_referral_tab.set_fields(patient_details)

    def get_check_list(self, chlist):
        results = {}
        for i in range(chlist.rowCount()):
            results[chlist.item(i).text()] = chlist.item(i).checkState()
        return results

