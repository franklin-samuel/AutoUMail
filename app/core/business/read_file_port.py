from abc import ABC, abstractmethod

from fastapi import UploadFile


class ReadFilePort(ABC):

    @abstractmethod
    async def read(self, file: UploadFile) -> str:
        pass