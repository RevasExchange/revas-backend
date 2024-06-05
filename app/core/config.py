from pydantic import EmailStr, BaseSettings

# from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Revas Exchange"
    PROJECT_VERSION: str = "1.0.0"

    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    ACCESS_TOKEN_EXPIRES_IN: int
    REFRESH_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str

    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr

    class Config:
        env_file = "./.env"


settings = Settings()
