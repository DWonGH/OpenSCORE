from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView


class RhythmTableWidget(QTableWidget):

    def __init__(self):
        super().__init__()
        self.setRowCount(0)
        self.setColumnCount(5)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        headers = ["Significance", "Spectral Freq", "Frequency (Hz)", "Amplitude (μV)", "Mod Effect"]
        self.setHorizontalHeaderLabels(headers)

    def new_rhythm(self, data):
        row = self.rowCount()
        self.insertRow(row)
        self.update_rhythm(data, row)

    def edit_rhythm(self, data):
        row = self.currentRow()
        self.update_rhythm(data, row)

    def delete_current_rhythm(self):
        row = self.currentRow()
        self.removeRow(row)

    def update_rhythm(self, data, row):
        significance = QTableWidgetItem(data["Significance"])
        spectral = QTableWidgetItem(data["Spectral frequency"])
        frequency = QTableWidgetItem(data["Frequency"])
        amplitude = QTableWidgetItem(data["Amplitude"])
        modulator = QTableWidgetItem(data["Modulator effect"])
        if significance is None:
            self.setItem(row, 0, QTableWidgetItem(""))
        else:
            self.setItem(row, 0, significance)
        if spectral is None:
            self.setItem(row, 0, QTableWidgetItem(""))
        else:
            self.setItem(row, 1, spectral)
        if frequency is None:
            self.setItem(row, 0, QTableWidgetItem(""))
        else:
            self.setItem(row, 2, frequency)
        if amplitude is None:
            self.setItem(row, 0, QTableWidgetItem(""))
        else:
            self.setItem(row, 3, amplitude)
        if modulator is None:
            self.setItem(row, 0, QTableWidgetItem(""))
        else:
            self.setItem(row, 4, modulator)
        self.item(row, 0).setTextAlignment(Qt.AlignHCenter)
        self.item(row, 1).setTextAlignment(Qt.AlignHCenter)
        self.item(row, 2).setTextAlignment(Qt.AlignHCenter)
        self.item(row, 3).setTextAlignment(Qt.AlignHCenter)
        self.item(row, 4).setTextAlignment(Qt.AlignHCenter)
        self.setCurrentIndex(self.model().index(row, 0))

    def current_rhythm(self):
        if self.rowCount() == 0:
            return False
        else:
            try:
                row = self.currentRow()
                return self.row_to_dict(row)
            except AttributeError:
                pass

    def table_to_dict(self):
        rows = []
        for i in range(self.rowCount()):
            rows.append(self.row_to_dict(i))
        print(rows)
        return rows

    def update_from_dict(self, data):
        self.setRowCount(0)
        for entry in data:
            self.new_rhythm(entry)

    def row_to_dict(self, row):
        data = {
            "Significance": self.item(row, 0).text(),
            "Spectral frequency": self.item(row, 1).text(),
            "Frequency": self.item(row, 2).text(),
            "Amplitude": self.item(row, 3).text(),
            "Modulator effect": self.item(row, 4).text()
        }
        return data