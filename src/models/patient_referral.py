

class Referral:

    def __init__(self):
        self.referrer_name = None  # I.e. physician
        self.referrer_details = None  # E.g. physician address & telephone
        self.diagnosis = None
        self.seizure_frequency = None
        self.last_seizure = None
        self.epilepsy_indications = None
        self.differential_indications = None
        self.paediatric_indications = None
        self.other_indications = None

    def update_from_dict(self, data):
        self.referrer_name = data['Referrer name']
        self.referrer_details = data['Referrer details']
        self.diagnosis = data['Diagnosis at referral']
        self.seizure_frequency = data['Seizure frequency']
        self.last_seizure = data['Time since last seizure']
        self.epilepsy_indications = data['Epilepsy-related indications']
        self.differential_indications = data['Other differential diagnostic questions']
        self.paediatric_indications = data['Specific paediatric indication']
        self.other_indications = data['Other indications']

    def to_dict(self):
        data = {
            "Referrer name": self.referrer_name,
            "Referrer details": self.referrer_details,
            "Diagnosis at referral": self.diagnosis,
            "Seizure frequency": self.seizure_frequency,
            "Time since last seizure": self.last_seizure,
            "Epilepsy-related indications": self.epilepsy_indications,
            "Other differential diagnostic questions": self.differential_indications,
            "Specific paediatric indication": self.paediatric_indications,
            "Other indications": self.other_indications
        }
        return data

    def set_to_nones(self):
        self.referrer_name = None
        self.referrer_details = None
        self.diagnosis = None
        self.seizure_frequency = None
        self.last_seizure = None
        self.epilepsy_indications = None
        self.differential_indications = None
        self.paediatric_indications = None
        self.other_indications = None
