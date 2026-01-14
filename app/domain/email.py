from dataclasses import dataclass
from typing import Optional


@dataclass
class Email:
    original_content: str
    processed_content: Optional[str]