"""Config for project"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Simple settings class for managing api keys"""

    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"))

    # api keys
    openai_api_key: str