from PyQt5.QtWidgets import QListView, QLineEdit, QFormLayout, QLabel, QWidget, QComboBox, QTextEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class PatientReferralWidget(QWidget):

    def __init__(self, parent=None):

        super(QWidget, self).__init__(parent)

        self.layout = QFormLayout()
        #self.layout.addRow(QLabel(""))

        # TODO: Add Address other contact info for referrer
        self.lbl_referrer_name = QLabel("Physician/ Referrer Name")
        self.lne_referrer_name = QLineEdit()
        self.layout.addRow(self.lbl_referrer_name, self.lne_referrer_name)

        self.lbl_referrer_details = QLabel("Referrer Details")
        self.txe_referrer_details = QTextEdit()
        self.layout.addRow(self.lbl_referrer_details, self.txe_referrer_details)

        self.lbl_diagnosis = QLabel("Diagnosis at referral")
        self.lne_diagnosis = QLineEdit()
        self.layout.addRow(self.lbl_diagnosis, self.lne_diagnosis)

        self.txt_seizure_freq = ["", "No Seizure", "Daily", "Bi-Daily", "Weekly", "Bi-Weekly", "Monthly", "Bi-Monthly", "Half Annually", "Yearly", "Previously"]
        self.lbl_seizure_freq = QLabel("Seizure frequency")
        self.cmb_seizure_freq = QComboBox()
        self.cmb_seizure_freq.addItems(self.txt_seizure_freq)
        self.layout.addRow(self.lbl_seizure_freq, self.cmb_seizure_freq)

        self.txt_last_seizure = ["", "Never", "Previous Day", "Previous 2 Days", "Previous Week", "Previous 2 Weeks", "Previous Month", "Previous 2 Months", "Previous 6 Months", "Previous Year", "Previously"]
        self.lbl_last_seizure = QLabel("Time since last seizure")
        self.cmb_last_seizure = QComboBox()
        self.cmb_last_seizure.addItems(self.txt_last_seizure)
        self.layout.addRow(self.lbl_last_seizure, self.cmb_last_seizure)

        #self.layout.addRow(QLabel(""))
        #self.layout.addRow(QLabel("Indication for EEG"))

        self.epilepsy_related_conditions = [
            "Clinical suspicion of epilepsy or seizure",
            "Changes in seizure pattern",
            "Suspicion of non-convulsive status epilepticus",
            "Reconsider the initial diagnosis of epilepsy",
            "Monitoring of status epilepticus",
            "Classification of a patient diagnosed with epilepsy",
            "Monitoring the effect of medication",
            "Monitoring of seizure frequency",
            "Presurgical evaluation",
            "Considering stopping AED therapy",
            "Drivers license or flight certificate"
        ]
        self.chlist_epilepsy = self.add_check_list("Epilepsy-related indications", self.epilepsy_related_conditions)

        self.other_differential_diagnostic_questions = [
            "Psychogenic non-epileptic seizures",
            "Encephalopathy",
            "Loss of consciousness",
            "Cerebral vascular disease",
            "Disturbance of consciousness",
            "Cerebral vascular disease",
            "Dementia",
            "Paroxysmal behavioral changes",
            "Other psychiatric or behavioral symptoms",
            "Coma",
            "Brain death",
        ]
        self.chlist_other_diagnostic = self.add_check_list("Other differential diagnostic questions",
                                                           self.other_differential_diagnostic_questions)

        self.specific_paediatric_indication = [
            "Genetic syndrome",
            "Metabolic disorder",
            "Regression",
            "Developmental problems"
        ]
        self.chlist_peadiatric = self.add_check_list("Specific paediatric indication",
                                                     self.specific_paediatric_indication)

        self.other_indication = [
            "Follow up EEG",
            "Research project",
            "Assessment of prognosis",
            "Other indication"
        ]
        self.chlist_other = self.add_check_list("Other indication", self.other_indication)

        self.setLayout(self.layout)

    def to_dict(self):
        data = {
            "Referrer name": self.lne_referrer_name.text(),
            "Referrer details": self.txe_referrer_details.toPlainText(),
            "Diagnosis at referral": self.lne_diagnosis.text(),
            "Seizure frequency": self.cmb_seizure_freq.currentText(),
            "Time since last seizure": self.cmb_last_seizure.currentText(),
            "Epilepsy-related indications": self.get_check_list(self.chlist_epilepsy),
            "Other differential diagnostic questions": self.get_check_list(self.chlist_other_diagnostic),
            "Specific paediatric indication": self.get_check_list(self.chlist_peadiatric),
            "Other indications": self.get_check_list(self.chlist_other)
        }
        return data

    def update_from_dict(self, data):
        self.lne_referrer_name.setText(data["Referrer name"])
        self.txe_referrer_details.setText(data["Referrer details"])
        self.lne_diagnosis.setText(data["Diagnosis at referral"])
        if data["Seizure frequency"] is None:
            self.cmb_seizure_freq.setCurrentIndex(0)
        else:
            self.cmb_seizure_freq.setCurrentIndex(self.txt_seizure_freq.index(data["Seizure frequency"]))
        if data["Time since last seizure"] is None:
            self.cmb_last_seizure.setCurrentIndex(0)
        else:
            self.cmb_last_seizure.setCurrentIndex(self.txt_last_seizure.index(data["Time since last seizure"]))

        erc = data["Epilepsy-related indications"]
        if erc is None:
            self.reset_check_list(self.chlist_epilepsy)
        else:
            self.set_check_list(self.chlist_epilepsy, erc)

        oddq = data["Other differential diagnostic questions"]
        if oddq is None:
            self.reset_check_list(self.chlist_other_diagnostic)
        else:
            self.set_check_list(self.chlist_other_diagnostic, oddq)

        spi = data["Specific paediatric indication"]
        if spi is None:
            self.reset_check_list(self.chlist_peadiatric)
        else:
            self.set_check_list(self.chlist_peadiatric, spi)

        other = data["Other indications"]
        if other is None:
            self.reset_check_list(self.chlist_other)
        else:
            self.set_check_list(self.chlist_other, other)

    def set_check_list(self, chlist, dict):
        for i in range(chlist.rowCount()):
            chlist.item(i).setCheckState(dict[chlist.item(i).text()])

    def get_check_list(self, chlist):
        results = {}
        for i in range(chlist.rowCount()):
            results[chlist.item(i).text()] = chlist.item(i).checkState()
        return results

    def reset_check_list(self, chlist):
        for i in range(chlist.rowCount()):
            chlist.item(i).setCheckState(0)

    def add_check_list(self, list_title, option_list):
        self.layout.addRow(QLabel(""))
        self.layout.addRow(QLabel(list_title))
        list_view = QListView()
        list_model = QStandardItemModel(list_view)

        for option in option_list:
            item = QStandardItem(option)
            item.setCheckable(True)
            list_model.appendRow(item)
        list_view.setModel(list_model)
        self.layout.addRow(list_view)
        return list_model