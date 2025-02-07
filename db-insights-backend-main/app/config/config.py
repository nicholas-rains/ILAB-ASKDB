import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

environment = os.environ.get("ENVIRONMENT", "local")

class Settings(BaseSettings):
    app_name: str = "DB-Insights"
    app_version: str = "0.1.0"
    app_description: str = "DB Insights API"
    reload: bool = True
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 5006
    log_config: str = "log_config_default.json"
    azure_openai_endpoint: str = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_deployment: str = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
    azure_openai_api_key: str = os.environ.get("AZURE_OPENAI_API_KEY")
    azure_openai_version: str = os.environ.get("AZURE_OPENAI_VERSION")
    pg_host: str = os.environ.get("PG_HOST")
    pg_user: str = os.environ.get("PG_USER_NAME")
    pg_port: int = os.environ.get("PG_PORT")
    pg_database: str = os.environ.get("PG_DATABASE")
    pg_password: str = os.environ.get("PG_PASSWORD")

  

class LocalSettings(Settings):
    host:str = "0.0.0.0"
    port:int = 5006
    log_level: str = "INFO"
    log_file: str = "app.log"
    azure_subscription_key: str = ""
    azure_endpoint: str = ""

class QaSettings(Settings):
    host: str = ""
    port: int = 5006
    debug: bool = False
    log_level: str = "INFO"
    log_file: str = "app.log"
    azure_subscription_key: str = ""
    azure_endpoint: str = ""

class ProductionSettings(Settings):
    host: str = ""
    port: int = 5006
    debug: bool = False
    log_level: str = "INFO"
    log_file: str = "app.log"
    azure_subscription_key: str = ""
    azure_endpoint: str = ""

def get_settings() -> Settings:
    if environment == "local":
        return LocalSettings()
    elif environment == "qa":
        return QaSettings()
    elif environment == "prod":
        return ProductionSettings()
    else:
        raise ValueError(f"Unknown environment: {environment}")
