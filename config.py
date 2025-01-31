from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str = ""
    items_per_user: int = 50

    debug: bool
    port: int
    # ENCRYPT_SECRET: str
    # JWT_SECRET: str
    encrypt_secret: str
    jwt_secret: str
    # SQLALCHEMY_DATABASE_URI: str
    # SQLALCHEMY_TRACK_MODIFICATIONS: bool
    sqlalchemy_database_uri: str
    sqlalchemy_track_modifications: bool

    # model_config = SettingsConfigDict(env_file=".env")
    class Config:
        env_file = ".env"  # Ensure you're loading the environment variables from an .env file


settings = Settings()
