"""
Probability visualization component.

Renders a full-width, modern horizontal breakdown of class
probabilities, with the top (predicted) class visually emphasized.
All values come directly from the backend's `probabilities` dict.
"""

from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

from utils.markup import render_html

NO_TUMOR_LABEL = "no tumor"

ProbList = List[Tuple[str, float]]


def render_probability_bars(result: Optional[Dict[str, Any]]) -> None:
    """Render the class probability breakdown.

    Args:
        result: The backend's /predict response dict containing a
            `probabilities` mapping, or None.
    """
    probabilities = (result or {}).get("probabilities")
    if not probabilities:
        return

    ordered: ProbList = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
    top_label = ordered[0][0]

    rows = "".join(_render_row(label, prob, label == top_label) for label, prob in ordered)

    with st.container(key="probability_bars", border=True):
        render_html('<div class="card-title">Class Probabilities</div>')
        render_html(rows)


def _render_row(label: str, prob: float, is_top: bool) -> str:
    """Build one probability row as an HTML string (not rendered yet —
    all rows are joined and rendered in a single call)."""
    pct = prob * 100
    tone = "success" if label.strip().lower() == NO_TUMOR_LABEL else "danger"
    row_class = "prob-row prob-row-top" if is_top else "prob-row"
    badge = '<span class="prob-badge">Predicted</span>' if is_top else ""
    return f"""
        <div class="{row_class}">
            <div class="prob-label"><span>{label}</span>{badge}</div>
            <div class="prob-track">
                <div class="prob-fill tone-{tone}" style="width:{pct}%;"></div>
            </div>
            <span class="prob-value">{pct:.1f}%</span>
        </div>
        """
