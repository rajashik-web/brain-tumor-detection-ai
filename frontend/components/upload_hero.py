"""
Upload hero component.

The primary, full-width call to action shown before any scan has been
analyzed — this is the focal point of the page, per the "upload
experience should be the main focus" design goal.

Uses st.container(key="upload_hero", border=True). Passing border=True
guarantees Streamlit always renders the bordered wrapper DOM node (the
plain default st.container() can skip it), which style.css then
targets defensively with both a direct class selector and a :has()
selector — see style.css for why both are used.
"""

from typing import Any, Dict, Optional

import streamlit as st
from PIL import Image

from api.client import predict_tumor
from utils.markup import render_html


def render_upload_hero() -> None:
    """Render the hero upload card: dropzone, hint text, and — once a
    file is selected — a preview plus the Analyze call to action."""
    with st.container(key="upload_hero", border=True):
        render_html(
            """
            <div class="hero-eyebrow">MRI ANALYSIS</div>
            <h2 class="hero-title">Upload a Brain MRI Scan</h2>
            <p class="hero-subtitle">
                Get an instant AI-assisted classification across four
                diagnostic categories, powered by a deep learning model.
            </p>
            """
        )

        uploaded_file = st.file_uploader(
            "Upload MRI scan",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed",
            key="hero_uploader",
        )
        # No extra hint paragraph here: Streamlit's own dropzone already
        # shows "Limit 200MB per file • PNG, JPG, JPEG" — repeating it
        # in a second line of text was redundant clutter, not polish.

        if uploaded_file is not None:
            _render_ready_state(uploaded_file)

        _render_error_if_any()


def _render_ready_state(uploaded_file) -> None:
    """Show the selected scan alongside the Analyze button.

    The file extension filter on st.file_uploader only checks the
    filename, not the actual content — a renamed or corrupted file
    can still reach here and make PIL raise. Without this guard that
    would surface as a raw Python traceback instead of a clean
    in-app error message.
    """
    try:
        image = Image.open(uploaded_file)
        image.verify()
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)  # re-open: verify() consumes the file
    except Exception:  # noqa: BLE001 - any decode failure means "not a valid image"
        st.error(
            f"'{uploaded_file.name}' couldn't be read as an image. "
            "Please upload a valid PNG or JPG file."
        )
        return

    image_bytes = uploaded_file.getvalue()

    preview_col, action_col = st.columns([1, 1.3], gap="large", vertical_alignment="center")
    with preview_col:
        st.image(image, use_container_width=True)
    with action_col:
        render_html(
            f"""
            <div class="hero-ready-label">Ready to analyze</div>
            <div class="hero-filename">{uploaded_file.name}</div>
            """
        )
        _render_analyze_button(image_bytes, uploaded_file.name)


def _render_analyze_button(image_bytes: bytes, filename: str) -> None:
    """Call the backend on click and store the result for the
    transformed post-analysis layout to pick up."""
    is_analyzing = st.session_state.get("analyzing", False)

    if st.button(
        "🔬 Analyze Scan",
        use_container_width=True,
        disabled=is_analyzing,
        key="hero_analyze_button",
    ):
        st.session_state["analyzing"] = True
        with st.spinner("Analyzing MRI..."):
            try:
                result: Optional[Dict[str, Any]] = predict_tumor(image_bytes, filename)
                st.session_state["prediction_result"] = result
                st.session_state["uploaded_image_bytes"] = image_bytes
                st.session_state["uploaded_filename"] = filename
                st.session_state["prediction_error"] = None
            except Exception as exc:  # noqa: BLE001 - surfaced to the user, not swallowed
                st.session_state["prediction_error"] = str(exc)
        st.session_state["analyzing"] = False
        # Force an immediate rerun so the layout transforms to the
        # result view right away, instead of waiting for the next
        # user interaction.
        st.rerun()


def _render_error_if_any() -> None:
    """Surface a backend/network failure instead of failing silently."""
    error = st.session_state.get("prediction_error")
    if error:
        st.error(f"Analysis failed: {error}")
