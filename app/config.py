from pydantic import BaseModel


class Settings(BaseModel):
    SMLMV: float = 1_423_500
    VIGENCIA_CONSULTA_DIAS: int = 30
    SCORE_MINIMO_PRODUCTO: float = 500
    PARTICIPACION_MINIMA_SEGUNDO_SOLICITANTE: float = 0.20
    MORA_MAXIMA_SEGUNDO_SOLICITANTE_SMLMV: float = 0.5


settings = Settings()
