import asyncio
from concurrent.futures import ThreadPoolExecutor
from transformers import pipeline

from exception import ProcessingFailedError
from models import AnalysisResult, Sentiment

thread_pool = ThreadPoolExecutor()
sentiment_pipeline = pipeline("sentiment-analysis")

"""
Analyzer function that performs sentiment analysis on
a string of text. 
"""
async def analyze(text: str) -> AnalysisResult:
    try:
        result = await asyncio.get_event_loop().run_in_executor(
            thread_pool, sentiment_pipeline, text
        )

        return AnalysisResult(
            label=Sentiment(result[0]['label']),
            score=result[0]['score']
        )
    except Exception as e:
        raise ProcessingFailedError("Failed to Process")