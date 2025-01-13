from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    ODDS_API_KEY: str = Field(description="Odds API api key", default="")


config = Config()
