from typing import Optional
from fastapi import Form, UploadFile

class ClassifyEmailFileRequest:
    def __init__(
        self,
        file: Optional[UploadFile] = Form(None)
    ):
        self.file = file