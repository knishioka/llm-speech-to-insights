# LLM Speech to Insights

A tool that integrates Google Cloud Speech-to-Text and Large Language Models to analyze English conversations and provide learning insights.

## Overview

LLM Speech to Insights takes audio recordings of English conversations (e.g., from language lessons) and:

1. Transcribes the speech to text using Google Cloud Speech-to-Text API
2. Summarizes the conversation content
3. Analyzes the English usage to provide personalized feedback on:
   - Grammar issues
   - Vocabulary usage
   - Pronunciation concerns
   - Fluency
   - Improvement recommendations

## Installation

### Prerequisites
- Python 3.11+
- Google Cloud Account with Speech-to-Text API enabled
- OpenAI API key

### Setting up the environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-speech-to-insights.git
cd llm-speech-to-insights
```

2. Install dependencies using Poetry:
```bash
pip install poetry
poetry install
```

3. Create a `.env` file with your API credentials (see `.env.sample` for reference):
```
GOOGLE_APPLICATION_CREDENTIALS="path/to/your/google-credentials.json"
GOOGLE_CLOUD_PROJECT="your-google-cloud-project-id"
OPENAI_API_KEY="your-openai-api-key"
```

## Usage

### Command Line Interface

Run the tool from the command line:

```bash
poetry run python -m src.main --bucket_name your-gcs-bucket-name --audio_file_path path/to/audio/file.webm
```

Options:
- `--bucket_name`: (Required) Name of the Google Cloud Storage bucket to temporarily store audio files
- `--audio_file_path`: (Required) Path to the audio file to analyze
- `--language_code`: (Optional) Language code for transcription (default: en-US)
- `--no_cleanup`: (Optional) Flag to keep the uploaded file in GCS after processing

### Example Output

The tool will output:
1. The full transcript of the conversation
2. A concise summary of the conversation
3. Detailed English learning insights including:
   - Grammar errors with corrections
   - Vocabulary improvements
   - Pronunciation issues
   - Fluency analysis
   - Actionable learning recommendations

## Project Structure

```
llm-speech-to-insights/
├── .env.sample                 # Environment variables template  
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
├── pyproject.toml              # Poetry dependency file
└── src/                        # Source code directory
    ├── __init__.py             # Package initialization
    ├── config.py               # Configuration settings
    ├── main.py                 # Main application entry point
    ├── storage/                # Storage related modules
    │   ├── __init__.py
    │   └── gcs_manager.py      # Google Cloud Storage operations
    ├── transcription/          # Transcription related modules
    │   ├── __init__.py
    │   └── speech_to_text.py   # Speech-to-text operations
    └── analysis/               # Analysis related modules
        ├── __init__.py
        ├── summarizer.py       # Conversation summarization
        └── insights_analyzer.py # English skills insights analyzer
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.