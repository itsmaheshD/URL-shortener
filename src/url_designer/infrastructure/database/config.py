from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url:str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings=Settings()

def get_database_url():
    return settings.database_url


