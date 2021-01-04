import unittest

from tests.models.test_main_model import TestMainModel
from tests.models.test_patient_details import TestPatientDetails
from tests.models.test_patient_referral import TestPatientReferral
from tests.models.test_recording_conditions import TestRecordingConditions

from tests.views.test_main_window import TestMainWindow
from tests.views.test_patient_details import TestPatientDetailsView
from tests.views.test_patient_referral import TestPatientReferralView
from tests.views.test_recording_conditions import TestRecordingConditionsView

from tests.controllers.test_main_window_controller import TestMainWindowController


class MasterTest(unittest.TestCase):

    def setUp(self) -> None:
        # Models
        self.test_main_model = TestMainModel()
        self.test_patient_details = TestPatientDetails()
        self.test_patient_referral = TestPatientReferral()
        self.test_recording_conditions = TestRecordingConditions()

        # Views
        self.test_main_window = TestMainWindow()
        self.test_patient_details_view = TestPatientDetailsView()
        self.test_patient_referral_view = TestPatientReferralView()
        self.test_recording_conditions_view = TestRecordingConditionsView()

        # Controllers
        self.test_main_window_controller = TestMainWindowController()


if __name__ == "__main__":
    unittest.main()