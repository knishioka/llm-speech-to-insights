"""
Configuration settings for the application.
"""

import os
from typing import Any, Dict

# Constants
GOOGLE_SPEECH_TO_TEXT_TIMEOUT = 1200  # 20 minutes timeout for speech to text operations

# Configuration mapping
CONFIG: Dict[str, Any] = {
    "google_application_credentials": os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS", ""
    ),
    "google_cloud_project": os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
    "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
    "speech_to_text": {
        "timeout": GOOGLE_SPEECH_TO_TEXT_TIMEOUT,
        "encoding": "WEBM_OPUS",
        "sample_rate_hertz": 16000,
        "language_code": "en-US",
        "enable_automatic_punctuation": True,
    },
}
