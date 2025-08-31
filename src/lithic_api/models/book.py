"""This module is still in development and will remain undocumented."""

from pydantic import BaseModel

from .assignments import Problem
from .vocabulary import Word


class Speaker(BaseModel):
    name: str
    statement: str
    question: str


class Conversation(BaseModel):
    speakers: list[Speaker]


class Lesson(BaseModel):
    subject: str
    topic: str
    conversations: list[Conversation]
    words: list[Word]


class Page(BaseModel):
    number: int
    lessons: list[Lesson]
    problems: list[Problem]
    words: list[Word]


class Chapter(BaseModel):
    number: int
    pages: list[Page]


class Book(BaseModel):
    chapters: list[Chapter]
