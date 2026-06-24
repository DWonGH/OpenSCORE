"""Small reusable widget helpers for the score_schema-backed tabs."""

from PyQt5.QtWidgets import QComboBox


def enum_combo(enum_cls, blank=True):
    """A combo box listing an enum's values (with a leading blank for 'unset')."""
    combo = QComboBox()
    if blank:
        combo.addItem("")
    for member in enum_cls:
        combo.addItem(member.value)
    return combo


def combo_enum(combo, enum_cls):
    """Return the selected enum member, or None when blank."""
    text = combo.currentText()
    return enum_cls(text) if text else None


def set_combo_text(combo, value):
    """Select the item matching an enum member / string (blank if None)."""
    combo.setCurrentText(value.value if hasattr(value, "value") else (value or ""))
