"""Transcript recording modules for building vocabulary sheets from youtube videos"""

from enum import StrEnum

from odmantic import Model
from pydantic import BaseModel

from .vocabulary import Vocabulary


class AvailableTranscriptLanguage(StrEnum):
    """Available languages to search for transcripts for"""

    KOREAN = "ko"
    ENGLISH = "en"


class VideoTranslationSubmission(BaseModel):
    """Submission model for youtube translation"""

    link: str
    target_language: AvailableTranscriptLanguage


class TranslatedYoutubeVideo(VideoTranslationSubmission):
    """Model for storing resulting translated video data"""

    vocabulary: Vocabulary


class TranslatedYoutubeVideoDocument(TranslatedYoutubeVideo, Model):
    """Simple ODMantic holding spot."""
