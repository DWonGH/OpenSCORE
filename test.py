import unittest

from tests.controllers.test_clinical_comments import TestClinicalCommentsController
from tests.controllers.test_diagnostic_significance import TestClinicalDiagnosticSignificanceController
from tests.controllers.test_patient_details import TestPatientDetailsController
from tests.controllers.test_patient_referral import TestPatientReferralController
from tests.controllers.test_recording_conditions import TestRecordingConditionsController
from tests.models.test_clinical_comments import TestClinicalComments
from tests.models.test_diagnostic_significance import TestDiagnosticSignificance
from tests.models.test_main_window import TestMainModel
from tests.models.test_patient_details import TestPatientDetails
from tests.models.test_patient_referral import TestPatientReferral
from tests.models.test_recording_conditions import TestRecordingConditions
from tests.views.test_clinical_comments import TestClinicalCommentsWidget
from tests.views.test_diagnostic_significance import TestDiagnosticSignificanceWidget

from tests.views.test_main_window import TestMainWindow
from tests.views.test_patient_details import TestPatientDetailsView
from tests.views.test_patient_referral import TestPatientReferralView
from tests.views.test_recording_conditions import TestRecordingConditionsView

from tests.controllers.test_main_window import TestMainWindowController


class MasterTest(unittest.TestCase):

    def setUp(self) -> None:
        # Models
        self.test_main_model = TestMainModel()
        self.test_patient_details = TestPatientDetails()
        self.test_patient_referral = TestPatientReferral()
        self.test_recording_conditions = TestRecordingConditions()
        self.test_diagnostic_significance = TestDiagnosticSignificance()
        self.test_clinical_comments_view = TestClinicalComments()

        # Views
        self.test_main_window = TestMainWindow()
        self.test_patient_details_view = TestPatientDetailsView()
        self.test_patient_referral_view = TestPatientReferralView()
        self.test_recording_conditions_view = TestRecordingConditionsView()
        self.test_diagnostic_significance_view = TestDiagnosticSignificanceWidget()
        self.test_clinical_comments_view = TestClinicalCommentsWidget()

        # Controllers
        self.test_main_window_controller = TestMainWindowController()
        self.test_patient_details_controller = TestPatientDetailsController()
        self.test_patient_referral_controller = TestPatientReferralController()
        self.test_recording_conditions_controller = TestRecordingConditionsController()
        self.test_diagnostic_significance_controller = TestClinicalDiagnosticSignificanceController()
        self.test_clinical_comments_controller = TestClinicalCommentsController()



if __name__ == "__main__":
    unittest.main()