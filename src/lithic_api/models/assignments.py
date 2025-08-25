from datetime import datetime
from enum import StrEnum


from pydantic import Field, BaseModel
from odmantic import Model


class ProblemType(StrEnum):
    """Simple enum for holding problem types"""
    SHORT_ANSWER = "short-answer"
    MULTIPLE_CHOICE = "multiple-choice"
    LONG_ANSWER = "long-answer"

class Problem(BaseModel):
    """A problem in a given assignment that may or may not have an answer"""
    question: str
    type: ProblemType
    answer: str = ""
    options: list[str] = Field(default_factory=list)


class SimpleAssignment(BaseModel):
    """A simple assignment.
    
    Usually a set of multiple choice
    or short form answers provided on a single piece of paper."""
    name: str
    problems: list[Problem]
    created: datetime = Field(default_factory=datetime.now)


class SimpleAssignmentModel(SimpleAssignment, Model):
    """DB wrapper for pydantic models"""


# 