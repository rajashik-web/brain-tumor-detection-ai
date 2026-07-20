"""Utility for injecting the external CSS file into the Streamlit page."""

from pathlib import Path

import streamlit as st


def load_css(relative_path: str) -> None:
    """
    Read a CSS file and inject it into the page inside a <style> tag.

    Args:
        relative_path: Path to the CSS file, relative to the project
            root (the directory containing app.py) — e.g.
            "styles/style.css".
    """
    project_root = Path(__file__).resolve().parent.parent
    css_path = project_root / relative_path
    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
