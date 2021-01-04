

class Patient:

    def __init__(self):
        self.name = None
        self.id = None
        self.dob = None
        self.gender = None
        self.handedness = None
        self.address = None  # TODO: Leaving this out as not important atm
        self.medication = None
        self.history = None

    def update_from_dict(self, data):
        self.name = data['Patient name']
        self.id = data['Patient ID']
        self.dob = data['Patient DOB']
        self.gender = data['Patient gender']
        self.handedness = data['Patient handedness']
        self.address = data['Patient address']
        self.medication = data['Patient medication']
        self.history = data['Patient history']

    def to_dict(self):
        data = {
            "Patient name": self.name,
            "Patient ID": self.id,
            "Patient DOB": self.dob,
            "Patient gender": self.gender,
            "Patient handedness": self.handedness,
            "Patient address": self.address,
            "Patient medication": self.medication,
            "Patient history": self.history
        }
        return data

    def set_to_nones(self):
        self.name = None
        self.id = None
        self.dob = None
        self.gender = None
        self.handedness = None
        self.address = None
        self.medication = None
        self.history = None