"""
Analyzer for generating English learning insights from conversation transcripts.
"""

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class EnglishInsightsAnalyzer:
    """Analyzer for generating English learning insights."""

    def __init__(
        self, model_name: str = "gpt-3.5-turbo-1106", temperature: float = 0.2
    ):
        """
        Initialize the insights analyzer.

        Args:
            model_name: Name of the OpenAI model to use
            temperature: Temperature parameter for the LLM
        """
        self.llm = ChatOpenAI(temperature=temperature, model_name=model_name)

        # Create the prompt template for analysis
        self.analysis_prompt = PromptTemplate(
            input_variables=["transcript"],
            template="""
            You are an expert English language tutor analyzing a transcript from an English conversation lesson.
            
            Transcript:
            {transcript}
            
            Please provide a detailed analysis of the student's English language skills, including:
            
            1. Grammar: Identify 3-5 grammar mistakes or areas for improvement with examples and corrections.
            2. Vocabulary: Highlight limited vocabulary usage and suggest 3-5 alternative expressions or words.
            3. Pronunciation: Note any pronunciation issues that might affect comprehension.
            4. Fluency: Analyze hesitations, fillers, and overall speech flow.
            5. Overall strengths: What aspects of English is the student good at?
            6. Specific improvement suggestions: Provide 3 actionable recommendations.
            
            Format your response in clear sections with examples from the transcript.
            """,
        )

        # Create the chain for analysis
        self.analysis_chain = LLMChain(llm=self.llm, prompt=self.analysis_prompt)

    def analyze_transcript(self, transcript: str) -> str:
        """
        Analyze a conversation transcript for English learning insights.

        Args:
            transcript: The conversation transcript text

        Returns:
            Analysis with insights and recommendations for improvement
        """
        result = self.analysis_chain.invoke({"transcript": transcript})
        return result["text"]
