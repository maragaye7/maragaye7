from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "MGA API"
    environment: str = "development"
    dolibarr_base_url: str = "https://mgassistances.com/crm"
    dolibarr_api_url: str = "https://mgassistances.com/crm/api/index.php"
    dolibarr_api_key: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    mga_admin_username: str = "admin"
    mga_admin_password: str
    cors_origins: str = "http://localhost:8081,http://localhost:19006"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

settings = Settings()
