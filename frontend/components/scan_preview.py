"""
Scan preview component.

Shown in the left column once a scan has been analyzed — a large
preview of the exact image that was sent to the backend, plus a way
to start over with a different scan.
"""

import io

import streamlit as st
from PIL import Image

from utils.markup import render_html


def render_scan_preview() -> None:
    """Render the large post-analysis MRI preview panel."""
    with st.container(key="scan_preview", border=True):
        render_html('<div class="card-title">MRI Scan</div>')

        image_bytes = st.session_state.get("uploaded_image_bytes")
        filename = st.session_state.get("uploaded_filename", "scan")

        if image_bytes:
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, use_container_width=True)
            render_html(f'<p class="scan-filename">{filename}</p>')

        if st.button(
            "↺ Analyze a Different Scan",
            use_container_width=True,
            key="reset_button",
        ):
            for key in (
                "prediction_result",
                "uploaded_image_bytes",
                "uploaded_filename",
                "prediction_error",
            ):
                st.session_state.pop(key, None)
            st.rerun()
