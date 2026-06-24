from score_schema import HyperventilationQuality, ModulatorsAndProcedures
from src.views.modulators import ModulatorsWidget, get_ternary, set_ternary


class ModulatorsController:
    """SCORE §4 — Modulators and procedures. Binds the view to a score_schema model."""

    def __init__(self):
        self.model = ModulatorsAndProcedures()
        self.view = ModulatorsWidget()

    def update_model(self):
        v, m = self.view, self.model
        m.photic_stimulation = get_ternary(v.cmb_photic)
        m.photic_effect = v.lne_photic_effect.text() or None
        m.hyperventilation = get_ternary(v.cmb_hv)
        quality = v.cmb_hv_quality.currentText()
        m.hyperventilation_quality = HyperventilationQuality(quality) if quality else None
        m.hyperventilation_effect = v.lne_hv_effect.text() or None
        m.sleep_deprivation = get_ternary(v.cmb_sleep_dep)
        m.natural_sleep = get_ternary(v.cmb_natural_sleep)
        m.induced_sleep = get_ternary(v.cmb_induced_sleep)
        m.awakening = get_ternary(v.cmb_awakening)
        m.medication_administered = v.lne_med_admin.text() or None
        m.medication_withdrawn = v.lne_med_withdrawn.text() or None
        m.other_modulators = v.lne_other.text() or None

    def update_view(self):
        v, m = self.view, self.model
        set_ternary(v.cmb_photic, m.photic_stimulation)
        v.lne_photic_effect.setText(m.photic_effect or "")
        set_ternary(v.cmb_hv, m.hyperventilation)
        v.cmb_hv_quality.setCurrentText(m.hyperventilation_quality.value if m.hyperventilation_quality else "")
        v.lne_hv_effect.setText(m.hyperventilation_effect or "")
        set_ternary(v.cmb_sleep_dep, m.sleep_deprivation)
        set_ternary(v.cmb_natural_sleep, m.natural_sleep)
        set_ternary(v.cmb_induced_sleep, m.induced_sleep)
        set_ternary(v.cmb_awakening, m.awakening)
        v.lne_med_admin.setText(m.medication_administered or "")
        v.lne_med_withdrawn.setText(m.medication_withdrawn or "")
        v.lne_other.setText(m.other_modulators or "")
