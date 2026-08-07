import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


class Settings(BaseModel):
    SMLMV: float = 1_423_500
    VIGENCIA_CONSULTA_DIAS: int = 30
    SCORE_MINIMO_PRODUCTO: float = 500
    PARTICIPACION_MINIMA_SEGUNDO_SOLICITANTE: float = 0.20
    MORA_MAXIMA_SEGUNDO_SOLICITANTE_SMLMV: float = 0.5

    EXPERIAN_CLIENT_ID: str = os.getenv("EXPERIAN_CLIENT_ID", "")
    EXPERIAN_CLIENT_SECRET: str = os.getenv("EXPERIAN_CLIENT_SECRET", "")
    EXPERIAN_OKTA_USERNAME: str = os.getenv("EXPERIAN_OKTA_USERNAME", "")
    EXPERIAN_OKTA_PASSWORD: str = os.getenv("EXPERIAN_OKTA_PASSWORD", "")
    EXPERIAN_SUBSCRIBER_USER: str = os.getenv("EXPERIAN_SUBSCRIBER_USER", "")
    EXPERIAN_SUBSCRIBER_PASSWORD: str = os.getenv("EXPERIAN_SUBSCRIBER_PASSWORD", "")
    EXPERIAN_SERVER_IP: str = os.getenv("EXPERIAN_SERVER_IP", "")
    EXPERIAN_CHANNEL_NAME: str = os.getenv("EXPERIAN_CHANNEL_NAME", "CONEXRED-01")
    EXPERIAN_CHANNEL_TYPE: str = os.getenv("EXPERIAN_CHANNEL_TYPE", "42")
    EXPERIAN_ENV: str = os.getenv("EXPERIAN_ENV", "uat")

    # Valor Ingreso — usa Okta OAuth2 separado
    EXPERIAN_VI_CLIENT_ID: str = os.getenv("EXPERIAN_VI_CLIENT_ID", "")
    EXPERIAN_VI_CLIENT_SECRET: str = os.getenv("EXPERIAN_VI_CLIENT_SECRET", "")
    EXPERIAN_VI_OKTA_USERNAME: str = os.getenv("EXPERIAN_VI_OKTA_USERNAME", "")
    EXPERIAN_VI_OKTA_PASSWORD: str = os.getenv("EXPERIAN_VI_OKTA_PASSWORD", "")
    EXPERIAN_VI_SUBSCRIBER_NIT: str = os.getenv("EXPERIAN_VI_SUBSCRIBER_NIT", "")
    EXPERIAN_VI_SUBSCRIBER_NAME: str = os.getenv("EXPERIAN_VI_SUBSCRIBER_NAME", "")
    EXPERIAN_VI_TOKEN_URL: str = os.getenv(
        "EXPERIAN_VI_TOKEN_URL",
        "https://experian-latamb.oktapreview.com/oauth2/ausdbwi7pes71n0hU0h7/v1/token",
    )
    EXPERIAN_VI_BASE_URL: str = os.getenv(
        "EXPERIAN_VI_BASE_URL",
        "https://demo-servicesesb.datacredito.com.co:444",
    )

    @property
    def experian_base_url(self) -> str:
        if self.EXPERIAN_ENV == "uat":
            return "https://uat-api.datacredito.com.co"
        return "https://api.datacredito.com.co"


settings = Settings()
