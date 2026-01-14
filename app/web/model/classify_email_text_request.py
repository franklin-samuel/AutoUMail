from typing import Optional
from fastapi import Form

class ClassifyEmailTextRequest:
    def __init__(
        self,
        text: Optional[str] = Form(None),
    ):
        self.text = text
