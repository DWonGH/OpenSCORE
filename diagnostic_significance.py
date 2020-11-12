from PyQt5.QtGui import QFont, QColor

from standard_item import StandardItem


def get_node():

    diagnostic_significance = StandardItem('Diagnostic significance', 16, set_bold=True, color=QColor(155, 0, 0))

    epilepsy = StandardItem('Epilepsy', 16, set_bold=True, color=QColor(155, 0, 0))
    epilepsy.appendRow(StandardItem('Psychogenic non-epileptic seizures (PNES)', 14, checkable=True))
    epilepsy.appendRow(StandardItem('Other non-epileptic clinical episode', 14, checkable=True))

    epilepticus = StandardItem('Status epilepticus', 16, set_bold=True, color=QColor(155, 0, 0))
    epilepticus.appendRow(StandardItem('Focal dysfunction of the central nervous system', 14, checkable=True))
    epilepticus.appendRow(StandardItem('Diffuse dysfunction of the central nervous system', 14, checkable=True))

    csws_eses = StandardItem('Continuous spikes and waves during slow sleep (CSWS) or electrical status epilepticus '
                             'in sleep (ESES)', 16, set_bold=True, color=QColor(155, 0, 0))
    csws_eses.appendRow(StandardItem('Coma', 14, checkable=True))
    csws_eses.appendRow(StandardItem('Brain death', 14, checkable=True))
    csws_eses.appendRow(StandardItem('EEG abnormality of uncertain significance', 14, checkable=True))

    diagnostic_significance.appendRow(epilepsy)
    diagnostic_significance.appendRow(epilepticus)
    diagnostic_significance.appendRow(csws_eses)

    return diagnostic_significance