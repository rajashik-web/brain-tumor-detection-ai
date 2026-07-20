"""
Brain Tumor Detection AI — Streamlit frontend entry point.

Orchestrates page config and component rendering only.
- All markup lives in components/
- All styling lives in styles/style.css
- All network calls live in api/client.py

Layout: before a scan is analyzed, the full-width upload hero is the
only thing on the page. Once `prediction_result` is set, the layout
transforms into the two-column results view plus the probability and
clinical summary sections below it.
"""

import streamlit as st

from components.clinical_summary import render_clinical_summary
from components.footer import render_footer
from components.header import render_header
from components.model_details import render_model_details
from components.prediction_panel import render_prediction_panel
from components.probability_bars import render_probability_bars
from components.scan_preview import render_scan_preview
from components.upload_hero import render_upload_hero
from utils.style_loader import load_css

st.set_page_config(
    page_title="Brain Tumor Detection AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css("styles/style.css")
render_header()

result = st.session_state.get("prediction_result")

if result is None:
    render_upload_hero()
else:
    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        render_scan_preview()
    with right:
        render_prediction_panel(result)
    render_probability_bars(result)
    render_clinical_summary(result)

render_model_details()
render_footer()
