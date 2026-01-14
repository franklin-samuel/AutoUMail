from abc import ABC, abstractmethod

from app.domain.classification import Classification
from app.domain.email import Email


class EmailClassifierPort(ABC):

    @abstractmethod
    async def classify(self, email: Email) -> Classification:
        pass