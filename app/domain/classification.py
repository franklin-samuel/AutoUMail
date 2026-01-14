from dataclasses import dataclass

from app.domain.enums.category import Category


@dataclass
class Classification:
    category: Category
    suggested_response: str