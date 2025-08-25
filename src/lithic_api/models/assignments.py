from datetime import datetime
from enum import StrEnum

from odmantic import Field, Model


class ProblemType(StrEnum):
    """Simple enum for holding problem types"""
    SHORT_ANSWER = "short-answer"
    MULTIPLE_CHOICE = "multiple-choice"
    LONG_ANSWER = "long-answer"

class Problem(Model):
    """A problem in a given assignment that has """
    question: str
    type: ProblemType
    answer: str = ""
    options: list[str] = Field(default_factory=list)


class SimpleAssignment(Model):
    """A simple assignment.
    
    Usually a set of multiple choice
    or short form answers provided on a single piece of paper."""
    name: str
    created: datetime = Field(default_factory=datetime.now)
    problems = list[Problem]
