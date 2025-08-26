"""Simple file for dealing with vocabulary"""

from odmantic import Model
from pydantic import BaseModel


class Word(BaseModel):
    """A vocabulary word"""

    word: str
    translation: str
    language: str
    to_language: str
    infinitive: str = ""


class Vocabulary(BaseModel):
    """A vocabulary page"""

    words: list[Word]
    title: str = ""
    page: int = 0


class VocabularySheet(BaseModel):
    """Effectively a document of vocab words."""

    title: str
    pages: list[Vocabulary]


class VocabularySheetDocument(VocabularySheet, Model):
    """Simple odmantic document for storage"""
