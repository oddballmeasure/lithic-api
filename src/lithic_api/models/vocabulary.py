"""Simple file for dealing with vocabulary"""

from enum import StrEnum

from odmantic import Model
from pydantic import BaseModel


class PartOfSpeech(StrEnum):
    """Identifier of what part of speech the word is used for."""

    NOUN = "noun"
    PRONOUN = "pronoun"
    NUMERAL = "numeral"
    VERB = "verb"
    ADJECTIVE = "adjective"
    DETERMINER = "determiner"
    ADVERB = "adverb"
    PARTICLE = "particle"
    EXCLAMATION = "exclamation"


class Word(BaseModel):
    """A vocabulary word"""

    word: str
    translation: str
    language: str
    to_language: str
    part_of_speech: PartOfSpeech
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
