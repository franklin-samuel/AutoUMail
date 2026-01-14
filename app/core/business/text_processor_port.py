from abc import ABC, abstractmethod


class TextProcessorPort(ABC):

    async def process(self, text: str) -> str:
        pass