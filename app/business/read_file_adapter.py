from io import BytesIO

from fastapi import UploadFile
import os
import PyPDF2

from app.core.business.read_file_port import ReadFilePort
from app.domain.exception.business_exception import BusinessException


class ReadFileAdapter(ReadFilePort):


    async def read(self, file: UploadFile) -> str:
        try:
            extension = os.path.splitext(file.filename)[1].lower()
            content_bytes = await file.read()

            if extension == '.txt':
                return content_bytes.decode('utf-8')

            elif extension == '.pdf':
                pdf_reader = PyPDF2.PdfReader(BytesIO(content_bytes))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text.strip()

            else:
                raise BusinessException(
                    f"Formato de arquivo não suportado: {extension}. "
                    "Use .txt ou .pdf"
                )

        except Exception as e:
            raise Exception(f"Erro ao ler arquivo: {str(e)}")