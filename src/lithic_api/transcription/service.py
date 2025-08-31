"""Simple wrapper for the yt transcript api."""

from urllib.parse import parse_qs, urlparse

from pydantic import BaseModel
from youtube_transcript_api import (NoTranscriptFound, TranscriptsDisabled,
                                    TranslationLanguageNotAvailable,
                                    YouTubeTranscriptApi)
from youtube_transcript_api.formatters import Formatter, TextFormatter

from lithic_api.models import AvailableTranscriptLanguage
from lithic_api.openai import BASE_TRANSLATION_PROMPT, OpenAIClient


class TranslationError(Exception):
    """Simple error handler"""


class YoutubeTranslationClient:
    """A simple utility class for parsing transcripts from youtube
    and getting the resulting Vocabulary from openai."""

    def __init__(
        self,
        link: str,
        languages: list[AvailableTranscriptLanguage] | None = None,
        formatter: Formatter | None = None,
    ):

        self.original_link = link

        self.video = self._parse_video(video=link)
        self.client = YouTubeTranscriptApi()
        self.formatter = formatter

        if not languages:
            self.languages = [AvailableTranscriptLanguage.ENGLISH]
        else:
            self.languages = [AvailableTranscriptLanguage(x) for x in languages]

        if not self.formatter:
            self.formatter = TextFormatter()

    def _parse_video(self, video: str) -> str:
        """Simple video ID gathering function

        Args:
            video (str): Video link to get id from

        Raises:
            TranslationError: If unable to find the link value (v=<id>) then error out

        Returns:
            str: video id value as a string.
        """
        parsed = urlparse(video)

        query = parse_qs(parsed.query)

        if "v" not in query.keys():
            raise TranslationError("No video id found in query")

        return query["v"][0]

    def process(
        self,
        response_model: type[BaseModel],
        video: str | None = None,
        languages: list[AvailableTranscriptLanguage] | None = None,
    ) -> BaseModel:
        """

        Args:
            response_model (BaseModel): Model to use for translation output. May be a subclass of pydantic BaseModel
            video (str | None, optional): video link defaults to internal link if none provided.
            languages (list[AvailableTranscriptLanguage] | None, optional): languages to search for translation. Defaults to internal language if none provided.

        Raises:
            TranslationError:

        Returns:
            response_model: The specific response model indicated in the top
        """
        if languages:
            self.languages = languages

        if video:
            self.video = self._parse_video(video)

        if self.formatter is None:
            self.formatter = TextFormatter()

        ai_client = OpenAIClient()
        try:
            transcript = self.client.fetch(
                self.video, languages=[language.value for language in self.languages]  # type: ignore[union-attr]
            )
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            raise TranslationError(
                "There was no transcript or it was disabled for the specified video."
            ) from e
        except TranslationLanguageNotAvailable as e:
            raise TranslationError(
                f"Translation language `{languages}` for video: `{self.video}` not available "
            ) from e

        formatted = self.formatter.format_transcript(transcript)

        result = ai_client.parse_user_prompt(
            system_prompt=BASE_TRANSLATION_PROMPT,
            user_prompt=formatted,
            response_model=response_model,
        )

        if not result:
            raise TranslationError("Unable to process video into vocabulary.")

        return result
