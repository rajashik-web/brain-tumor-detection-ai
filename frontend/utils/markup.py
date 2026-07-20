"""
Shared helper for rendering raw HTML blocks in Streamlit.

Streamlit's markdown renderer treats any line indented 4+ spaces as a
Markdown code block, which silently prints raw HTML as literal text
instead of rendering it. This helper dedents before handing the string
to st.markdown, and enforces the "one complete block per call" rule:
never open a tag in one render_html() call and close it in another —
each st.markdown() call is an isolated DOM node, so a tag opened in
one cannot be closed in the next.
"""

import textwrap
import streamlit as st


def render_html(html: str) -> None:
    """
    Render HTML safely inside Streamlit.

    Removes indentation so HTML isn't interpreted as a Markdown code block.
    """

    st.markdown(
        textwrap.dedent(html).strip(),
        unsafe_allow_html=True,
    )
