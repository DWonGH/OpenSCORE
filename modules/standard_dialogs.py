from PyQt5.QtWidgets import QMessageBox, QLineEdit, QWidget
import re

def confirmation_dialog(title, message, icon):
    """
    Produces a pop-up with a specified message that the user confirms or cancels
    :param title:
    :param message:
    :param icon:
    :return: The result code of the chosen button e.g. 1024 == confirmed
    """
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    #msg.setInformativeText("This is additional information")
    #msg.setDetailedText("The details are as follows:")

    return msg.exec_()


def message_dialog(title, message, icon, detailed_text=None):
    """
    Produces a pop-up with a specified message for the user
    :param title:
    :param message:
    :param icon:
    :param detailed_text:
    :return:
    """
    try:
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.Ok)
        if detailed_text:
            msg.setDetailedText(str(detailed_text))
            #msg.setInformativeText("This is additional information")
        return msg.exec_()
    except Exception as e:
        print(e)


class DateLineEdit(QLineEdit):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.user_input = ""
        self.setPlaceholderText("e.g. 13-12-2020")
        self.textEdited.connect(self.hdl_txt_edited)

    def hdl_txt_edited(self, text):
        """
        We want to ignore any other input than numbers
        There must be 8 digits
        Take only the first 8 digits
        If there are

        1. remove any other symbols
        2. remove any symbols from string longer than 8
        3. save the number only string to user_input
        4. generate a display string with dashes
        5. update the lineedit with the display string
        :param text:
        :return:
        """
        #print(text)
        if "--" in text:
            text = text.replace('--', '-')

        text = re.sub("\d\d^-\d\d")
        text = re.sub("[^0-9]", "", text)

        if len(text) == 2:
            text += '-'


        self.setText(text)
        print(text)
