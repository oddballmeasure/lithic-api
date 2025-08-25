"""OpenAI Helper client. Wraps useful functionality"""

from enum import StrEnum
from pathlib import Path
from typing import Any, BinaryIO

from openai import OpenAI
from openai.types.file_object import FileObject
from pydantic import BaseModel

from lithic_api.config import Settings

config = Settings() # type: ignore[call-arg]

class FilePurpose(StrEnum):
    USER_DATA = "user-data"
    VISION = "vision"
    FINE_TUNE = "fine-tune"
    EVALS = "evals"
    ASSISTANTS = "assistants"
    BATCH = "batch"


class OpenAIClient:
    """A simple OpenAI Wrapper for performing api commands"""
    def __init__(self, api_key: str | None = None, model: str = config.openai_model):

        self.api_key = config.openai_api_key

        if api_key:
            self.api_key = api_key

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    

    def _get_structured_output(self, system_prompt: str, user_prompt: dict[str, Any], response_model: BaseModel) -> BaseModel | None:
        """A generic method for getting structured output responses from openai."""

        # Ignored types below because they're what openai 
        # tells me to expect but mypy doesn't like that
        results = self.client.responses.parse(model=self.model,
                                    input = [
                                        {"role": "system",
                                         "content": system_prompt},
                                         user_prompt # type: ignore[list-item]
                                    ],
                                    text_format=response_model) # type: ignore[arg-type]
        
        return results.output_parsed
    

    def upload_file(self, file: str | BinaryIO | Path, purpose: FilePurpose = FilePurpose.USER_DATA) -> FileObject:
        """Upload"""
        if isinstance(file, (str, Path)):
            file = Path(file).open('rb')
        

        return self.client.files.create(file=file, purpose=purpose) # type: ignore[arg-type]
    

    def parse_user_prompt(self, system_prompt: str, user_prompt: str, response_model: BaseModel) -> BaseModel | None:
        """Take a user prompt and run an openai structured output parse using a model they provide."""
        return self._get_structured_output(system_prompt=system_prompt, user_prompt={'role': "user", "content": user_prompt}, response_model=response_model)

    def parse_user_file(self, system_prompt: str, file: str | BinaryIO | Path, response_model: BaseModel, purpose=FilePurpose.USER_DATA) -> BaseModel | None:
        """Take a user file and run an openai structured output parse using a model they provide.""" 
        file_result = self.upload_file(file=file, purpose=purpose)

        user_prompt = {'role': "user",
                       'content': {"type": "input_file", 
                                   "file_id": file_result.id}}

        return self._get_structured_output(system_prompt=system_prompt, user_prompt=user_prompt, response_model=response_model)