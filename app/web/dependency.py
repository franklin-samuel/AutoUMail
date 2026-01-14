import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi.params import Depends

from app.business.email_classifier_adapter import EmailClassifierAdapter
from app.business.read_file_adapter import ReadFileAdapter
from app.core.business.email_classifier_port import EmailClassifierPort
from app.core.business.read_file_port import ReadFilePort
from app.core.infrastructure.gemini_service_port import GeminiServicePort
from app.core.infrastructure.text_processor_port import TextProcessorPort
from app.infrastructure.gemini_service_adapter import GeminiServiceAdapter
from app.infrastructure.text_processor_adapter import TextProcessorAdapter

load_dotenv()

def get_gemini_service_port() -> GeminiServicePort:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    return GeminiServiceAdapter(api_key=gemini_api_key)

def get_text_processor_port() -> TextProcessorPort:
    return TextProcessorAdapter()

def get_read_file_port() -> ReadFilePort:
    return ReadFileAdapter()

def get_email_classifier_port(
        gemini_service: Annotated[GeminiServicePort, Depends(get_gemini_service_port)],
        text_processor: Annotated[TextProcessorPort, Depends(get_text_processor_port)],
) -> EmailClassifierPort:
    return EmailClassifierAdapter(
        gemini_service=gemini_service,
        text_processor=text_processor
    )