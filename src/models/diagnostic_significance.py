

class DiagnosticSignificance:

    def __init__(self):
        self.diagnosis = None  # e.g. normal, abnormal, nor definite abnormality
        self.abnormal_specification = None

    def to_dict(self):
        data = {
            "Diagnosis": self.diagnosis,
            "Abnormal specification": self.abnormal_specification
        }
        return data

    def update_from_dict(self, data):
        self.diagnosis = data["Diagnosis"]
        self.abnormal_specification = data["Abnormal specification"]

    def set_to_nones(self):
        self.diagnosis = None
        self.abnormal_specification = None