"""OpenAI Client tests"""

from pathlib import Path

import pytest

from lithic_api.models import SimpleAssignment
from lithic_api.openai import SIMPLE_ASSIGNMENT_PROMPT, OpenAIClient


def test_simple_assignment(test_data_dir: Path):
    """Upload a simple assignment to OpenAI and get back the results"""

    assignment = test_data_dir / "korean_assignment_1.pdf"

    client = OpenAIClient()

    result: SimpleAssignment = client.parse_user_file(
        system_prompt=SIMPLE_ASSIGNMENT_PROMPT,
        file=assignment,
        response_model=SimpleAssignment,
    )

    assert len(result.problems) == 27

    problem = result.problems[0]

    assert problem.question == "I came to Korea."
    assert problem.answer_context is not None
    assert problem.answer is not None
