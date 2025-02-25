"""
Main entry point for the LLM English Conversation Analyzer.
"""

import argparse
import logging
import os
from typing import Any, Dict, Optional

from src.analysis.insights_analyzer import EnglishInsightsAnalyzer
from src.analysis.summarizer import ConversationSummarizer
from src.storage.gcs_manager import GCSManager
from src.transcription.speech_to_text import SpeechToText

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def process_audio_file(
    bucket_name: str,
    audio_file_path: str,
    language_code: Optional[str] = "en-US",
    cleanup: bool = True,
) -> Dict[str, Any]:
    """
    Process an audio file through the entire pipeline.

    Args:
        bucket_name: Name of the GCS bucket
        audio_file_path: Path to the local audio file
        language_code: Language code for transcription
        cleanup: Whether to delete the uploaded file after processing

    Returns:
        Dictionary containing the transcript, summary, and insights
    """
    try:
        # Validate file existence
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        # Initialize components
        logger.info("Initializing components")
        gcs_manager = GCSManager(bucket_name)
        speech_to_text = SpeechToText()
        summarizer = ConversationSummarizer()
        insights_analyzer = EnglishInsightsAnalyzer()

        # Upload file to GCS
        logger.info(f"Uploading file {audio_file_path} to GCS bucket {bucket_name}")
        blob_name = os.path.basename(audio_file_path)
        gcs_uri = gcs_manager.upload_file(audio_file_path, blob_name)

        # Transcribe audio
        logger.info(f"Transcribing audio from {gcs_uri}")
        transcript = speech_to_text.transcribe_from_gcs(gcs_uri, language_code)

        # Generate summary
        logger.info("Generating conversation summary")
        summary = summarizer.summarize(transcript)

        # Analyze for English learning insights
        logger.info("Analyzing transcript for English learning insights")
        insights = insights_analyzer.analyze_transcript(transcript)

        # Cleanup if requested
        if cleanup:
            logger.info(f"Cleaning up: deleting {blob_name} from GCS")
            gcs_manager.delete_file(blob_name)

        # Return results
        return {"transcript": transcript, "summary": summary, "insights": insights}

    except Exception as e:
        logger.error(f"Error processing audio file: {str(e)}", exc_info=True)
        raise


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Analyze English conversation audio files for learning insights."
    )
    parser.add_argument(
        "--bucket_name", required=True, help="The name of the GCS bucket"
    )
    parser.add_argument(
        "--audio_file_path", required=True, help="The path to the audio file"
    )
    parser.add_argument(
        "--language_code",
        default="en-US",
        help="Language code for transcription (default: en-US)",
    )
    parser.add_argument(
        "--no_cleanup",
        action="store_true",
        help="Do not delete the uploaded file after processing",
    )

    args = parser.parse_args()

    try:
        result = process_audio_file(
            bucket_name=args.bucket_name,
            audio_file_path=args.audio_file_path,
            language_code=args.language_code,
            cleanup=not args.no_cleanup,
        )

        # Print results
        print("\n" + "=" * 50)
        print("TRANSCRIPT:")
        print("=" * 50)
        print(result["transcript"])

        print("\n" + "=" * 50)
        print("SUMMARY:")
        print("=" * 50)
        print(result["summary"])

        print("\n" + "=" * 50)
        print("ENGLISH LEARNING INSIGHTS:")
        print("=" * 50)
        print(result["insights"])

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
