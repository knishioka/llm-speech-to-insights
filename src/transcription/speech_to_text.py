"""
Speech-to-text operations using Google Cloud Speech API.
"""

from typing import Optional

from google.cloud import speech

from src.config import CONFIG


class SpeechToText:
    """Handler for speech-to-text operations."""

    def __init__(self):
        """Initialize the speech-to-text client."""
        self.client = speech.SpeechClient()
        self.config = CONFIG["speech_to_text"]

    def transcribe_from_gcs(
        self, gcs_uri: str, language_code: Optional[str] = None
    ) -> str:
        """
        Transcribe audio from a Google Cloud Storage URI.

        Args:
            gcs_uri: Google Cloud Storage URI for the audio file
            language_code: Language code for transcription (default: en-US)

        Returns:
            Transcribed text
        """
        audio = speech.RecognitionAudio(uri=gcs_uri)

        # Setup the recognition config
        config = speech.RecognitionConfig(
            encoding=getattr(
                speech.RecognitionConfig.AudioEncoding, self.config["encoding"]
            ),
            sample_rate_hertz=self.config["sample_rate_hertz"],
            language_code=language_code or self.config["language_code"],
            enable_automatic_punctuation=self.config["enable_automatic_punctuation"],
        )

        # Perform long-running speech recognition
        operation = self.client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=self.config["timeout"])

        # Combine all transcribed segments
        transcript = " ".join(
            [result.alternatives[0].transcript for result in response.results]
        )

        return transcript
