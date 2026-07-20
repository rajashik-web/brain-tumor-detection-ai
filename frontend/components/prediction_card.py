"""
Prediction card component.

Displays the predicted class, confidence, and inference time returned
by the backend. Every value shown here comes directly from the
`/predict` response — nothing is computed or invented client-side.

Each branch (empty state vs. result) is built as one complete HTML
string and rendered in a single call — see header.py's docstring for
why splitting a card's opening/closing <div> across separate
st.markdown() calls produces an empty styled box.
"""

from typing import Any, Dict, Optional

from utils.markup import render_html

NO_TUMOR_LABEL = "no tumor"


def render_prediction_card(result: Optional[Dict[str, Any]]) -> None:
    """
    Render the prediction results card.

    Args:
        result: The backend response dict (`prediction`, `confidence`,
            `inference_time`), or None if no analysis has run yet.
    """
    if result is None:
        render_html(
            """
            <div class="glass-card">
                <div class="card-title">🧬 Prediction Results</div>
                <div class="empty-state">
                    <div class="empty-icon">🔍</div>
                    <p>Upload and analyze a scan to see results</p>
                </div>
            </div>
            """
        )
        return

    prediction = str(result.get("prediction", "Unknown"))
    confidence = float(result.get("confidence", 0.0))
    inference_time = float(result.get("inference_time", 0.0))

    is_healthy = prediction.strip().lower() == NO_TUMOR_LABEL
    badge_class = "badge-success" if is_healthy else "badge-danger"
    icon = "✅" if is_healthy else "⚠️"

    # NOTE: assumes `confidence` arrives as a 0-1 fraction. If your
    # backend already returns a percentage, drop the `* 100` below.
    render_html(
        f"""
        <div class="glass-card">
            <div class="card-title">🧬 Prediction Results</div>
            <div class="prediction-badge {badge_class}">
                <span>{icon}</span><span>{prediction}</span>
            </div>
            <div class="metric-row">
                <div class="metric-chip">
                    <span class="metric-value">{confidence * 100:.1f}%</span>
                    <span class="metric-label">Confidence</span>
                </div>
                <div class="metric-chip">
                    <span class="metric-value">{inference_time:.0f} ms</span>
                    <span class="metric-label">Inference Time</span>
                </div>
            </div>
        </div>
        """
    )
