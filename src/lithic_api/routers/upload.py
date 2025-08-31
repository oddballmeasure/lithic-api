"""
File upload router and api endpoints
"""

import tempfile

from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel

from lithic_api.models import SimpleAssignment, VocabularySheet
from lithic_api.openai import (
    BASE_TRANSLATION_PROMPT,
    SIMPLE_ASSIGNMENT_PROMPT,
    OpenAIClient,
)

router = APIRouter(prefix="/upload")


async def parse_uploaded_file(
    file: UploadFile, prompt: str, response_model: type[BaseModel]
) -> type[BaseModel] | None:
    """Do the actual uploading part (utility function to reduce code repetition)

    Args:
        file (UploadFile): file to convert to structured output
        prompt (str): prompt to use for instruction
        response_model (type[BaseModel]): output model

    Raises:
        None

    Returns:
        BaseModel | None: resulting model provided by response_model or None if it couldn't be processed.
    """
    client = OpenAIClient()

    file_extension = file.filename.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as f:
        f.write(file.file.read())

    result = client.parse_user_file(
        system_prompt=prompt,
        file=f.name,
        response_model=response_model,
    )

    return result


@router.post(path="/simple-assignment")
async def upload_simple_assignment(file: UploadFile) -> SimpleAssignment:
    """Post a simple assignment and return the assignment data back to the user.

    Args:
        file (UploadFile): The file you are uploading

    Raises:
        HTTPException: If unable to process the assignment, return an exception

    Returns:
        SimpleAssignment: A model detailing the questions the user is to complete
        and the answers for each of those questions (if available)
    """

    result: SimpleAssignment = await parse_uploaded_file(
        file, prompt=SIMPLE_ASSIGNMENT_PROMPT, response_model=SimpleAssignment
    )  # type: ignore[assignment]
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Unable to process your file for questions and answers.",
        )

    return result


@router.post(path="/vocabulary-sheet")
async def upload_vocabulary_sheet(file: UploadFile) -> VocabularySheet:
    """Upload a vocabulary sheet or file
       for building flash cards for studying.

    Args:
        file (UploadFile): Specific file to process

    Raises:
        HTTPException: If no sheet can be created, raise an error

    Returns:
        VocabularySheet: Resulting model detailing all words found in the sheet.
    """

    result: VocabularySheet = await parse_uploaded_file(
        file, prompt=BASE_TRANSLATION_PROMPT, response_model=VocabularySheet
    )  # type: ignore[assignment]
    if not result:
        raise HTTPException(
            status_code=400, detail="Unable to create a vocabulary sheet from page."
        )

    return result
