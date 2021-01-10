from PyQt5.QtWidgets import QLineEdit
import re


class IntegerLineEdit(QLineEdit):

    def __init__(self):
        super(QLineEdit, self).__init__()
        self.textEdited.connect(self.hdl_text_edited)

    def hdl_text_edited(self, text):
        getVals = list([val for val in text if val.isnumeric()])
        result = "".join(getVals)
        self.setText(result)


class FloatLineEdit(QLineEdit):

    def __init__(self):
        super(QLineEdit, self).__init__()
        self.fixed_text = ""
        self.textEdited.connect(self.hdl_text_edited)

    def hdl_text_edited(self, text):
        if not str(text).count('.') > 1:
            getVals = list([val for val in text if val is '.' or val.isnumeric()])
            self.fixed_text = "".join(getVals)
        self.setText(self.fixed_text)
