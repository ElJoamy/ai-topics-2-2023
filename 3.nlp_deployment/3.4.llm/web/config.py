from enum import Enum
from functools import cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class GPTModel(str, Enum):
    gpt_4 = "gpt-4"
    gpt_3_5_turbo = "gpt-3.5-turbo"



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    service_name: str = "Project Idea Generator"
    log_level: str = "DEBUG"
    openai_key: str
    model: GPTModel = GPTModel.gpt_3_5_turbo
    

@cache
def get_settings():
    return Settings()