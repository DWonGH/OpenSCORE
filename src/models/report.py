import copy

from pydantic import ValidationError

from src.models.background_activity import BackgroundActivity
from src.models.clinical_comments import ClinicalComments
from src.models.diagnostic_significance import DiagnosticSignificance
from src.models.patient_details import Patient
from src.models.patient_referral import Referral
from src.models.recording_conditions import RecordingConditions
from score_schema import (
    SCHEMA_VERSION,
    EegReport,
    Episodes,
    InterictalFindings,
    ModulatorsAndProcedures,
    SleepAndDrowsiness,
)


def _blanks_to_none(obj):
    """Return a copy of a nested dict/list with empty strings replaced by None.

    Legacy GUI widgets emit ``""`` for an unset field; score_schema treats unset as None.
    Used only to build a *validation* copy — the saved file keeps the legacy shape.
    """
    if isinstance(obj, dict):
        return {k: _blanks_to_none(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_blanks_to_none(v) for v in obj]
    return None if obj == "" else obj


class Report:

    def __init__(self, model=None):
        self.model = model

        # Existing sections — legacy, GUI-bound models (replaced by the controllers' own
        # model instances when wired up in MainWindowController).
        self.patient_details = Patient()
        self.patient_referral = Referral()
        self.recording_conditions = RecordingConditions()
        self.background_activity = BackgroundActivity()
        self.diagnostic_significance = DiagnosticSignificance()
        self.clinical_comments = ClinicalComments()

        # New SCORE modules — backed directly by score_schema models. GUI tabs are added
        # incrementally; until then these round-trip through the .score file unchanged.
        self.modulators = ModulatorsAndProcedures()
        self.sleep = SleepAndDrowsiness()
        self.interictal = InterictalFindings()
        self.episodes = Episodes()

    @staticmethod
    def _dump(model):
        return model.model_dump(mode="json", by_alias=True)

    def assemble_dict(self):
        """Build the full 11-section .score dict (legacy shape for the 6 original sections)."""
        return {
            "Schema version": SCHEMA_VERSION,
            "Patient details": self.patient_details.to_dict(),
            "Patient referral": self.patient_referral.to_dict(),
            "Recording conditions": self.recording_conditions.to_dict(),
            "Modulators and procedures": self._dump(self.modulators),
            "Background activity": self.background_activity.to_dict(),
            "Sleep and drowsiness": self._dump(self.sleep),
            "Interictal findings": self._dump(self.interictal),
            "Episodes": self._dump(self.episodes),
            "Diagnostic significance": self.diagnostic_significance.to_dict(),
            "Clinical comments": self.clinical_comments.to_dict(),
        }

    def validate(self):
        """Validate the current report against score_schema.

        Returns the pydantic ``EegReport`` on success, or raises ``ValidationError``.
        Operates on a blanks-as-None copy so empty GUI fields don't count as bad data.
        """
        return EegReport.from_score_dict(_blanks_to_none(copy.deepcopy(self.assemble_dict())))

    def to_dict(self):
        """The .score dict to write. Keeps the legacy shape (backward compatible); runs a
        best-effort schema validation and warns rather than blocking the save."""
        data = self.assemble_dict()
        try:
            self.validate()
        except ValidationError as e:
            print(f"[score_schema] report did not fully validate; saving anyway:\n{e}")
        return data

    def from_dict(self, data):
        try:
            EegReport.from_score_dict(_blanks_to_none(copy.deepcopy(data)))
        except ValidationError as e:
            print(f"[score_schema] loaded report did not fully validate:\n{e}")

        self.patient_details.update_from_dict(data['Patient details'])
        self.patient_referral.update_from_dict(data['Patient referral'])
        self.recording_conditions.update_from_dict(data['Recording conditions'])
        self.background_activity.update_from_dict(data["Background activity"])
        self.diagnostic_significance.update_from_dict(data['Diagnostic significance'])
        self.clinical_comments.update_from_dict(data['Clinical comments'])

        # New sections — tolerate older 6-section files that omit them.
        self.modulators = ModulatorsAndProcedures.model_validate(data.get("Modulators and procedures", {}))
        self.sleep = SleepAndDrowsiness.model_validate(data.get("Sleep and drowsiness", {}))
        self.interictal = InterictalFindings.model_validate(data.get("Interictal findings", {}))
        self.episodes = Episodes.model_validate(data.get("Episodes", {}))

    def reset(self):
        self.patient_details.set_to_nones()
        self.patient_referral.set_to_nones()
        self.recording_conditions.set_to_nones()
        self.background_activity.set_to_nones()
        self.diagnostic_significance.set_to_nones()
        self.clinical_comments.set_to_nones()
        self.modulators = ModulatorsAndProcedures()
        self.sleep = SleepAndDrowsiness()
        self.interictal = InterictalFindings()
        self.episodes = Episodes()
