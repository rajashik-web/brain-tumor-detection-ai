"""Header component: minimal branding and a live backend status pill."""

from api.client import check_backend_status
from utils.markup import render_html


def render_header() -> None:
    """Render the top bar with brand, tagline, and backend status.

    Deliberately minimal — no fabricated navigation links, since the
    app has no other pages to link to.
    """
    is_online = check_backend_status()
    status_class = "status-online" if is_online else "status-offline"
    status_text = "Backend Online" if is_online else "Backend Offline"

    render_html(
        f"""
        <div class="app-header">
            <div class="brand">
                <div class="brand-mark">🧠</div>
                <div>
                    <h1 class="brand-title">Brain Tumor Detection AI</h1>
                    <p class="brand-subtitle">AI-powered MRI Diagnosis</p>
                </div>
            </div>
            <div class="status-pill {status_class}">
                <span class="status-dot"></span>{status_text}
            </div>
        </div>
        """
    )
