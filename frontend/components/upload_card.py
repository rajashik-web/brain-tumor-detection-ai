"""
Upload card component.

Handles the drag-and-drop MRI upload, image preview, genuine image
metadata (format / dimensions / mode / size of the actual uploaded
file), and the Analyze action that calls the backend.

Wrapped in `st.container(key="upload_card")` rather than a manual
HTML <div>: this makes Streamlit itself emit one real DOM element
around the file_uploader/image/button widgets, which style.css then
styles as a glass card via the `.st-key-upload_card` selector. Manually
opening a <div> in one st.markdown() call and closing it in another
does not work here, because each st.markdown() call renders in its
own isolated container — the widgets in between end up outside the
div entirely, leaving an empty styled box and an unstyled widget.
"""

from typing import Any, Dict, Optional

import streamlit as st
from PIL import Image

from api.client import predict_tumor
from utils.markup import render_html


def render_upload_card() -> Optional[Dict[str, Any]]:
    """
    Render the upload card.

    Returns:
        The backend's prediction result dict if a scan has been
        analyzed (persisted across reruns via session_state), otherwise
        None.
    """
    with st.container(key="upload_card"):
        render_html('<div class="card-title">📤 Upload MRI Scan</div>')

        uploaded_file = st.file_uploader(
            "Upload MRI scan",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed",
            key="mri_uploader",
        )

        if uploaded_file is None:
            _render_empty_state()
            return None

        image = Image.open(uploaded_file)
        image_bytes = uploaded_file.getvalue()

        st.image(image, use_container_width=True)
        _render_image_info(image, uploaded_file.type, len(image_bytes))
        _render_analyze_button(image_bytes, uploaded_file.name)
        _render_error_if_any()

    return st.session_state.get("prediction_result")


def _render_empty_state() -> None:
    """Placeholder shown before any file is uploaded — states the two
    ways to add a scan and which formats are accepted."""
    render_html(
        """
        <div class="empty-state upload-empty-state">
            <div class="empty-icon">🩻</div>
            <p class="empty-title">Drag and drop an MRI scan here</p>
            <p class="empty-hint">or click above to browse &middot; PNG / JPG</p>
        </div>
        """
    )


def _render_image_info(image: Image.Image, mime_type: str, size_bytes: int) -> None:
    """Show real metadata for the actual uploaded image — format,
    dimensions, color mode, and file size — never placeholder values."""
    fmt = (image.format or mime_type.split("/")[-1]).upper()
    width, height = image.size
    size_kb = size_bytes / 1024
    render_html(
        f"""
        <div class="info-chip-row">
            <div class="info-chip">
                <span class="info-label">Format</span>
                <span class="info-value">{fmt}</span>
            </div>
            <div class="info-chip">
                <span class="info-label">Dimensions</span>
                <span class="info-value">{width}×{height}</span>
            </div>
            <div class="info-chip">
                <span class="info-label">Mode</span>
                <span class="info-value">{image.mode}</span>
            </div>
            <div class="info-chip">
                <span class="info-label">Size</span>
                <span class="info-value">{size_kb:.0f} KB</span>
            </div>
        </div>
        """
    )


def _render_analyze_button(image_bytes: bytes, filename: str) -> None:
    """Render the Analyze CTA with a status hint above it, disabled
    while a request is in flight, and call the backend on click."""
    is_analyzing = st.session_state.get("analyzing", False)

    render_html(
        '<p class="cta-hint">Scan loaded — ready to run detection</p>'
    )

    if st.button(
        "🔬 Analyze MRI Scan",
        use_container_width=True,
        disabled=is_analyzing,
        key="analyze_button",
    ):
        st.session_state["analyzing"] = True
        with st.spinner("Analyzing MRI..."):
            try:
                result = predict_tumor(image_bytes, filename)
                st.session_state["prediction_result"] = result
                st.session_state["prediction_error"] = None
            except Exception as exc:  # noqa: BLE001 - surfaced to the user, not swallowed
                st.session_state["prediction_result"] = None
                st.session_state["prediction_error"] = str(exc)
        st.session_state["analyzing"] = False


def _render_error_if_any() -> None:
    """Surface a backend/network failure instead of failing silently."""
    error = st.session_state.get("prediction_error")
    if error:
        st.error(f"Prediction failed: {error}")
