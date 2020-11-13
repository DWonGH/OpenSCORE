from PyQt5.QtWidgets import QFileDialog, QInputDialog, QLineEdit


def save_file(self):
    """
    File explorer pop up to choose file save locations
    :return:
    - String: The path describing the file location
    - None: If the user cancelled or did not select a valid path
    """
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    dialog = QFileDialog()
    dialog.setDefaultSuffix('json')
    fileName, _ = dialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", self.report_name,
                                         "JSON Files (*.json)", options=options)
    if fileName:
        print(fileName)
        return fileName
    else:
        return None


def open_file(self):
    """
    File explorer pop up to locate and open a ready made file
    :return:
    - String: The path describing the file location
    - None: If the user cancelled or did not select a valid path
    """
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    dialog = QFileDialog()
    dialog.setDefaultSuffix('json')
    fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                              "JSON Files (*.json)", options=options)
    if fileName:
        print(fileName)
        return fileName
    else:
        return None


def get_text(self, title, message):
    """
    Standard text retrieval for user input
    :param self:
    :param title: String - Pop up window name
    :param message: String - Pop up window message
    :return:
    - String: The users submitted text
    - None: If the user did not enter any text if something went wrong
    """
    text, okPressed = QInputDialog.getText(self, f"{title}", f"{message}", QLineEdit.Normal, "")
    if okPressed and text != '':
        print(text)
        return text
    else:
        return None