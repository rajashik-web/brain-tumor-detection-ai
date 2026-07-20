"""
Probability card component.

Renders the per-class probability breakdown as animated CSS bars and
an interactive Plotly horizontal bar chart. All values come straight
from the backend's `probabilities` dict — no synthetic data.

Wrapped in `st.container(key="probability_card")` because it contains
a real widget (`st.plotly_chart`) — see upload_card.py's module
docstring for why manual <div> open/close across separate
st.markdown() calls breaks around real widgets.
"""

from typing import Any, Dict, List, Optional, Tuple

import plotly.graph_objects as go
import streamlit as st

from utils.markup import render_html

NO_TUMOR_LABEL = "no tumor"
SUCCESS_COLOR = "#2ED47A"
DANGER_COLOR = "#FF5C73"

ProbList = List[Tuple[str, float]]


def render_probability_card(result: Optional[Dict[str, Any]]) -> None:
    """
    Render the probability breakdown card.

    Args:
        result: The backend response dict containing a `probabilities`
            mapping of {class_name: probability}, or None if no
            analysis has run yet.
    """
    with st.container(key="probability_card"):
        render_html('<div class="card-title">📊 Class Probabilities</div>')

        probabilities = (result or {}).get("probabilities")
        if not probabilities:
            render_html(
                """
                <div class="empty-state">
                    <div class="empty-icon">📈</div>
                    <p>Probability breakdown will appear here after analysis</p>
                </div>
                """
            )
            return

        ordered: ProbList = sorted(
            probabilities.items(), key=lambda item: item[1], reverse=True
        )

        _render_animated_bars(ordered)
        _render_probability_chart(ordered)


def _class_color(label: str) -> str:
    """Green for 'No Tumor', red for any tumor class."""
    return SUCCESS_COLOR if label.strip().lower() == NO_TUMOR_LABEL else DANGER_COLOR


def _render_animated_bars(ordered_probs: ProbList) -> None:
    """One animated CSS progress bar per class, widths set from real
    backend probabilities. Per-bar width/color are inherently dynamic
    data values, so they stay inline; every static rule (track, radius,
    animation) still lives in style.css."""
    rows = []
    for label, prob in ordered_probs:
        pct = prob * 100
        color = _class_color(label)
        rows.append(
            f"""
            <div class="bar-row">
                <div class="bar-label"><span>{label}</span><span>{pct:.1f}%</span></div>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{pct}%; background:{color};"></div>
                </div>
            </div>
            """
        )
    render_html("".join(rows))


def _render_probability_chart(ordered_probs: ProbList) -> None:
    """Interactive horizontal Plotly bar chart of the same probabilities."""
    labels = [label for label, _ in ordered_probs]
    values = [round(prob * 100, 1) for _, prob in ordered_probs]
    colors = [_class_color(label) for label in labels]

    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker=dict(color=colors),
            text=[f"{v}%" for v in values],
            textposition="outside",
        )
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", family="Manrope, sans-serif"),
        margin=dict(l=0, r=40, t=6, b=6),
        height=180 + 22 * len(labels),
        xaxis=dict(visible=False, range=[0, 100]),
        yaxis=dict(autorange="reversed"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
