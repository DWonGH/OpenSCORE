from PyQt5.QtWidgets import QMessageBox


def confirmation_dialog(title, message, icon):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(icon)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    #msg.setInformativeText("This is additional information")
    #msg.setDetailedText("The details are as follows:")

    return msg.exec_()


def message_dialog(title, message, icon, detailed_text=None):
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

