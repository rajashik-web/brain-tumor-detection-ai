"""Footer component: a minimal, elegant medical disclaimer."""

from utils.markup import render_html


def render_footer() -> None:
    """Render the closing disclaimer line."""
    render_html(
        """
        <div class="app-footer">
            <p>
                Brain Tumor Detection AI is a diagnostic support tool and
                does not replace professional medical evaluation.
            </p>
        </div>
        """
    )
