"""
Conversation summarization using LLM.
"""

from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI


class ConversationSummarizer:
    """Summarizer for conversation transcripts."""

    def __init__(self, model_name: str = "gpt-3.5-turbo-1106", temperature: float = 0):
        """
        Initialize the conversation summarizer.

        Args:
            model_name: Name of the OpenAI model to use
            temperature: Temperature parameter for the LLM
        """
        self.llm = ChatOpenAI(temperature=temperature, model_name=model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500, chunk_overlap=50
        )

    def summarize(self, text: str) -> str:
        """
        Summarize the conversation text.

        Args:
            text: The conversation transcript text

        Returns:
            Summarized text
        """
        docs = self.text_splitter.split_documents([Document(page_content=text)])
        chain = load_summarize_chain(self.llm, chain_type="stuff")

        summary_result = chain.invoke(docs)
        return summary_result["output_text"]
