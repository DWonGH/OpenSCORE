from PyQt5.QtGui import QFont, QColor

from standard_item import StandardItem


def get_node():

    font = 10
    diagnostic_significance = StandardItem('Diagnostic significance', font, set_bold=True)

    epilepsy = StandardItem('Epilepsy', font, set_bold=True)
    epilepsy.appendRow(StandardItem('Psychogenic non-epileptic seizures (PNES)', font, checkable=True))
    epilepsy.appendRow(StandardItem('Other non-epileptic clinical episode', font, checkable=True))

    epilepticus = StandardItem('Status epilepticus', font, set_bold=True)
    epilepticus.appendRow(StandardItem('Focal dysfunction of the central nervous system', font, checkable=True))
    epilepticus.appendRow(StandardItem('Diffuse dysfunction of the central nervous system', font, checkable=True))

    csws_eses = StandardItem('Continuous spikes and waves during slow sleep (CSWS) \nor electrical status epilepticus '
                             'in sleep (ESES)', font, set_bold=True)
    csws_eses.appendRow(StandardItem('Coma', font, checkable=True))
    csws_eses.appendRow(StandardItem('Brain death', font, checkable=True))
    csws_eses.appendRow(StandardItem('EEG abnormality of uncertain significance', font, checkable=True))

    diagnostic_significance.appendRow(epilepsy)
    diagnostic_significance.appendRow(epilepticus)
    diagnostic_significance.appendRow(csws_eses)

    return diagnostic_significance