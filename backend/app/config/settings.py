from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration centralisee de MGA API, lue depuis les variables d'environnement.

    Aucune valeur secrete ne doit avoir de defaut exploitable en production :
    les defauts ci-dessous ne servent qu'au developpement local.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Dolibarr
    dolibarr_base_url: str = "https://mgassistances.com/crm"
    dolibarr_api_url: str = "https://mgassistances.com/crm/api/index.php"
    dolibarr_api_key: str = ""
    dolibarr_timeout_seconds: float = 10.0

    # Base de donnees locale
    database_url: str = "postgresql+psycopg2://mga:mga@localhost:5432/mga_api"

    # JWT
    jwt_secret_key: str = "dev-only-insecure-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 30

    # CORS
    cors_allowed_origins: str = "http://localhost:8081,http://localhost:19006"

    # App
    environment: str = "development"
    log_level: str = "INFO"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
