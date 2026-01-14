from abc import ABC, abstractmethod

from app.domain.classification import Classification


class GeminiServicePort(ABC):

    @abstractmethod
    async def classify_and_generate_response(self, text: str) -> Classification:
        pass