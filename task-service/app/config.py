from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    jwt_secret_key: str
    jwt_algorithm: str

    service_name: str
    service_port: int
    log_level: str

    db_pool_size: int
    db_max_overflow: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()  # <-- this line is essential!
