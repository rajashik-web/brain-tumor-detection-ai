from utils.markup import render_html

MODEL_INFO = {
    "Model": "EfficientNetB0",
    "Framework": "TensorFlow",
    "Classes": "4",
    "Input Size": "224 × 224",
    "Validation Accuracy": "87%",
}


def render_model_card() -> None:
    """Render model information."""

    chips = "".join(
        [
            f"""
<div class="model-chip">
    <span class="model-label">{label}</span>
    <span class="model-value">{value}</span>
</div>
"""
            for label, value in MODEL_INFO.items()
        ]
    )

    html = f"""
<div class="glass-card">
    <div class="card-title">
        ⚙️ Model Information
    </div>

    <div class="model-grid">
        {chips}
    </div>
</div>
"""

    render_html(html)