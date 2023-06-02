from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    api_username: str
    api_password: str
    api_url: HttpUrl
    module_name: str
    crypto_base_url: HttpUrl
    crypto_api_key: str
    db_hostname: str
    db_port: int
    db_password: str
    db_name: str
    db_username: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


app_settings = Settings()
