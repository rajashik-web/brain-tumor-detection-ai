"""
Model details component.

Static architecture metadata about the deployed model, tucked into a
native st.expander so it doesn't compete with the upload/prediction
experience for screen space (per the "do not waste screen space"
design goal).
"""

import streamlit as st
from utils.markup import render_html

MODEL_INFO = {
    "Model": "EfficientNetB0",
    "Framework": "TensorFlow",
    "Classes": "4",
    "Input Size": "224 × 224",
    "Validation Accuracy": "87%",
}


def render_model_details() -> None:
    """Render model architecture info inside a collapsible expander."""

    with st.expander("⚙️ Model Details", expanded=False):

        chips = "".join(
            f"""
<div class="model-chip">
    <span class="model-label">{label}</span>
    <span class="model-value">{value}</span>
</div>
"""
            for label, value in MODEL_INFO.items()
        )

        render_html(
            f"""
<div class="model-grid">
{chips}
</div>
"""
        )