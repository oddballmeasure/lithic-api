import pytest

from lithic_api.models import Vocabulary
from lithic_api.transcription import TranslationError, YoutubeTranslationClient

YT_PASS = "https://www.youtube.com/watch?v=lGrvrWIRNNQ"

YT_FAIL = "https://www.youtube.com/watch?v=sos93-v5sso&list=RDsos93-v5sso&start_radio=1"


def test_video_fails():
    """Test that translation fails for a video with no translation."""

    yt = YoutubeTranslationClient(link=YT_FAIL, languages=["ko"])

    with pytest.raises(TranslationError):
        yt.process(response_model=Vocabulary)


def test_video_passes():
    """Test that translation fails for a video with no translation."""

    yt = YoutubeTranslationClient(link=YT_PASS, languages=["ko"])

    result = yt.process(response_model=Vocabulary)

    assert isinstance(result, Vocabulary)
    assert len(result.words) > 0
