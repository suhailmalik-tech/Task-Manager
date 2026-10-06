from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config =  SettingsConfigDict(env_file=".env", extra = "ignore")

    DB_CONNECTION:str
    SECRET_KEY:str
    ALGORITHM:str
    EXPIRE_MINUTES:str

settings = Settings()