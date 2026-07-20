"""
Clinical summary component.

Generates a short, templated interpretation sentence from the
backend's own prediction and confidence — no invented findings. The
confidence "bucket" (high/moderate/low) is a plain threshold on the
real number, not a fabricated statistic.
"""

from typing import Any, Dict, Optional

import streamlit as st

from utils.markup import render_html

NO_TUMOR_LABEL = "no tumor"

HIGH_CONFIDENCE_THRESHOLD = 0.85
MODERATE_CONFIDENCE_THRESHOLD = 0.60


def render_clinical_summary(result: Optional[Dict[str, Any]]) -> None:
    """Render the AI interpretation card.

    Args:
        result: The backend's /predict response dict, or None.
    """
    if not result:
        return

    prediction = str(result.get("prediction", "Unknown"))
    confidence = float(result.get("confidence", 0.0))
    is_healthy = prediction.strip().lower() == NO_TUMOR_LABEL

    finding = _build_finding_sentence(prediction, confidence, is_healthy)

    with st.container(key="clinical_summary", border=True):
        render_html(
            f"""
            <div class="card-title">🩺 AI Interpretation</div>
            <p class="clinical-text">{finding}</p>
            <p class="clinical-disclaimer">
                This prediction should be reviewed by a qualified radiologist
                before any clinical decision is made.
            </p>
            """
        )


def _build_finding_sentence(prediction: str, confidence: float, is_healthy: bool) -> str:
    """Build the interpretation sentence from real prediction data."""
    if confidence >= HIGH_CONFIDENCE_THRESHOLD:
        confidence_word = "high"
    elif confidence >= MODERATE_CONFIDENCE_THRESHOLD:
        confidence_word = "moderate"
    else:
        confidence_word = "low"

    if is_healthy:
        return (
            "The uploaded MRI shows no findings consistent with the tumor "
            f"classes in this model, with {confidence_word} confidence "
            f"({confidence * 100:.1f}%)."
        )
    return (
        f"The uploaded MRI most closely matches <strong>{prediction}</strong> "
        f"with {confidence_word} confidence ({confidence * 100:.1f}%)."
    )
