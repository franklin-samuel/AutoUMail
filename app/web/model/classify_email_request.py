from typing import Optional
from fastapi import Form, UploadFile

class ClassifyEmailFileRequest:
    def __init__(
        self,
        file: Optional[UploadFile] = Form(None)
    ):
        self.file = file

class ClassifyEmailTextRequest:
    def __init__(
        self,
        text: Optional[str] = Form(None),
    ):
        self.text = text
