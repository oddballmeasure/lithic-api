"""Config for project"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Simple settings class for managing api keys"""

    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"))

    api_prefix: str
    # openai
    openai_model: str
    openai_api_key: str

    # Database info
    mongo_db: str
    mongo_host: str
    mongo_port: str
    mongo_user: str
    mongo_pass: str
