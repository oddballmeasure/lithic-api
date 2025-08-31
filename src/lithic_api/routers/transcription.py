"""
Transcription router and api endpoints
"""

from fastapi import APIRouter, HTTPException

from lithic_api.models import VideoTranslationSubmission, Vocabulary
from lithic_api.transcription import YoutubeTranslationClient

router = APIRouter(prefix="/transcript")


@router.post(path="/youtube-video")
async def generate_youtube_vocabulary(
    submission: VideoTranslationSubmission,
) -> Vocabulary:
    """Submit a link from youtube for transcript processing

    Args:
        link (str): The link to process
        languages (list[AvailableTranscriptLanguage]): Supported languages you want the type for

    Raises:
        HTTPException: If no vocabulary could be created, raise an error

    Returns:
        Vocabulary: the list of vocabulary words from the transcript for studying.
    """
    yt = YoutubeTranslationClient(
        link=submission.link, languages=[submission.target_language]
    )

    result: Vocabulary = yt.process(response_model=Vocabulary)  # type: ignore[assignment]

    if not result:
        raise HTTPException(
            status_code=400,
            detail="Unable to translate video, and no other errors occurred.",
        )

    return result
