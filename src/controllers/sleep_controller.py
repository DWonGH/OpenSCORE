from score_schema import SleepAndDrowsiness
from src.views.modulators import get_ternary, set_ternary
from src.views.sleep import SleepWidget, selected_items, set_selected


class SleepController:
    """SCORE §7 — Sleep and drowsiness. Binds the view to a score_schema model."""

    def __init__(self):
        self.model = SleepAndDrowsiness()
        self.view = SleepWidget()

    def update_model(self):
        v, m = self.view, self.model
        m.normal_graphoelements = selected_items(v.lst_graphoelements)
        m.achieved_stages = selected_items(v.lst_stages)
        m.abnormal_asymmetry = get_ternary(v.cmb_asymmetry)
        m.soremp = get_ternary(v.cmb_soremp)
        m.non_reactive_sleep = get_ternary(v.cmb_non_reactive)
        m.notes = v.lne_notes.text() or None

    def update_view(self):
        v, m = self.view, self.model
        set_selected(v.lst_graphoelements, m.normal_graphoelements)
        set_selected(v.lst_stages, m.achieved_stages)
        set_ternary(v.cmb_asymmetry, m.abnormal_asymmetry)
        set_ternary(v.cmb_soremp, m.soremp)
        set_ternary(v.cmb_non_reactive, m.non_reactive_sleep)
        v.lne_notes.setText(m.notes or "")
