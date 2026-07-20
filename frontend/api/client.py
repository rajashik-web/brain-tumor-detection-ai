"""
API client for the Brain Tumor Detection backend.

Untouched from the previous version — this is the only module that
talks to the network, and its contract with the backend has not
changed as part of this redesign.
"""

from __future__ import annotations

from typing import Any, Dict

import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"

PREDICT_TIMEOUT_SECONDS = 30
HEALTH_TIMEOUT_SECONDS = 2
HEALTH_CACHE_TTL_SECONDS = 5


def predict_tumor(image_bytes: bytes, filename: str = "scan.png") -> Dict[str, Any]:
    """
    Send an MRI image to the FastAPI `/predict` endpoint and return the
    parsed JSON response, unmodified.

    Expected backend response shape:
        {
            "prediction": str,
            "confidence": float,          # assumed 0-1
            "probabilities": dict[str, float],  # assumed 0-1 each
            "inference_time": float       # assumed milliseconds
        }

    Args:
        image_bytes: Raw bytes of the uploaded MRI image.
        filename: Original filename, forwarded for logging/content-type.

    Returns:
        The backend's JSON response as a dict.

    Raises:
        requests.exceptions.RequestException: on network/HTTP failure.
        ValueError: if the response body is not valid JSON.
    """
    files = {"file": (filename, image_bytes, "image/png")}
    response = requests.post(
        PREDICT_ENDPOINT, files=files, timeout=PREDICT_TIMEOUT_SECONDS
    )
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=HEALTH_CACHE_TTL_SECONDS, show_spinner=False)
def check_backend_status() -> bool:
    """
    Check whether the FastAPI backend is reachable.

    Used only to drive the header's live "Backend Online/Offline" pill —
    a genuine reachability check with a short timeout, not a fabricated
    or hardcoded badge. Cached for a few seconds so it doesn't fire a
    real network request (and its latency) on every single rerun —
    every button click and st.rerun() would otherwise re-check it.

    Returns:
        True if the server responded at all, False on any connection
        error or timeout.
    """
    try:
        requests.get(API_BASE_URL, timeout=HEALTH_TIMEOUT_SECONDS)
        return True
    except requests.exceptions.RequestException:
        return False
