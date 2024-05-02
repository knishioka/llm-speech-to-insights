import argparse

from google.cloud import speech, storage
from google.cloud.speech import RecognitionAudio, RecognitionConfig
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

GOOGLE_SPEECH_TO_TEXT_TIMEOUT = 1200


def upload_file_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Google Cloud Storageにファイルをアップロードする"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def delete_file_from_gcs(bucket_name, blob_name):
    """Google Cloud Storageからファイルを削除する"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    print(f"File {blob_name} deleted from GCS.")


def transcribe_from_gcs(gcs_uri, lang="en-US"):
    """GCSにアップロードされた音声ファイルを文字起こしする"""
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=16000,  # 適切に設定してください
        language_code=lang,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=GOOGLE_SPEECH_TO_TEXT_TIMEOUT)

    return " ".join([result.alternatives[0].transcript for result in response.results])


def summarize_conversation(text):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=50)
    docs = text_splitter.split_documents([Document(text)])
    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.invoke(docs)


def main(bucket_name, audio_file_path):
    blob_name = audio_file_path.split("/")[-1]
    gcs_uri = f"gs://{bucket_name}/{blob_name}"

    upload_file_to_gcs(bucket_name, audio_file_path, blob_name)
    transcription = transcribe_from_gcs(gcs_uri)
    print(transcription)
    summary = summarize_conversation(transcription)["output_text"]
    print("Summary:", summary)
    delete_file_from_gcs(bucket_name, blob_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload and transcribe audio files, then summarize the conversation."
    )
    parser.add_argument(
        "--bucket_name", required=True, help="The name of the GCS bucket"
    )
    parser.add_argument(
        "--audio_file_path", required=True, help="The path to the audio file"
    )

    args = parser.parse_args()

    main(args.bucket_name, args.audio_file_path)
