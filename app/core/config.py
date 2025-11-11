from pydantic import BaseSettings

class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
