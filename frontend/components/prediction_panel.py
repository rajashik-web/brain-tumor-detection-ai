"""
Prediction panel component.

Shown in the right column once a scan has been analyzed. Surfaces
every field the backend returns (prediction, confidence, inference
time), plus a risk label derived from the predicted class and the
static model name — nothing here is randomized or invented.
"""

from typing import Any, Dict

import streamlit as st

from utils.markup import render_html

NO_TUMOR_LABEL = "no tumor"
MODEL_NAME = "EfficientNetB0"  # kept in sync with components/model_details.py


def render_prediction_panel(result: Dict[str, Any]) -> None:
    """Render the prediction results panel.

    Args:
        result: The backend's /predict response dict.
    """
    prediction = str(result.get("prediction", "Unknown"))
    confidence = float(result.get("confidence", 0.0))
    inference_time = float(result.get("inference_time", 0.0))

    is_healthy = prediction.strip().lower() == NO_TUMOR_LABEL
    tone = "success" if is_healthy else "danger"
    risk_label = "Low Risk" if is_healthy else "Elevated Risk"
    icon = "✅" if is_healthy else "⚠️"

    # NOTE: assumes `confidence` is a 0-1 fraction and `inference_time`
    # is already in milliseconds, per api/client.py's docstring. Adjust
    # the formatting below if your backend's units differ.
    with st.container(key="prediction_panel", border=True):
        render_html(
            f"""
            <div class="card-title">Prediction Results</div>
            <div class="prediction-headline tone-{tone}">
                <span class="prediction-icon">{icon}</span>
                <span class="prediction-name">{prediction}</span>
            </div>
            <div class="confidence-row">
                <div class="confidence-track">
                    <div class="confidence-fill tone-{tone}" style="width:{confidence * 100:.1f}%;"></div>
                </div>
                <span class="confidence-value">{confidence * 100:.1f}%</span>
            </div>
            <div class="detail-grid">
                <div class="detail-item">
                    <span class="detail-label">Risk</span>
                    <span class="detail-value tone-{tone}">{risk_label}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Inference Time</span>
                    <span class="detail-value">{inference_time:.0f} ms</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Status</span>
                    <span class="detail-value tone-success">Completed</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Model</span>
                    <span class="detail-value">{MODEL_NAME}</span>
                </div>
            </div>
            """
        )
