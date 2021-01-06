

class ClinicalComments:

    def __init__(self):
        self.interpreter_name = None
        self.clinical_comments = None

    def to_dict(self):
        data = {
            "Interpreter name": self.interpreter_name,
            "Clinical comments": self.clinical_comments
        }
        return data

    def update_from_dict(self, data):
        self.interpreter_name = data["Interpreter name"]
        self.clinical_comments = data["Clinical comments"]

    def set_to_nones(self):
        self.interpreter_name = None
        self.clinical_comments = None