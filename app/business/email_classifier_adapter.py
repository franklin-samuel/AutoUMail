from app.core.business.email_classifier_port import EmailClassifierPort
from app.core.infrastructure.gemini_service_port import GeminiServicePort
from app.core.infrastructure.text_processor_port import TextProcessorPort
from app.domain.classification import Classification
from app.domain.email import Email


class EmailClassifierAdapter(EmailClassifierPort):

    def __init__(self, gemini_service: GeminiServicePort, text_processor: TextProcessorPort):
        self.gemini_service = gemini_service
        self.text_processor = text_processor

    async def classify(self, email: Email) -> Classification:
        try:
            processed_text = await self.text_processor.process(email.original_content)
            email.processed_content = processed_text

            classification = await self.gemini_service.classify_and_generate_response(
                email.processed_content
            )

            return classification

        except Exception as e:
            raise Exception(f"Erro ao classificar email: {str(e)}")