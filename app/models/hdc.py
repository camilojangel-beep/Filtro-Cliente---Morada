from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Union
from enum import Enum


class LineaCredito(str, Enum):
    TDC = "TDC"
    ROT = "ROT"
    CAB = "CAB"
    VIV = "VIV"
    SOSTENIMIENTO = "SOSTENIMIENTO"


# Mapping de accountType de Experian HDC+ → línea de crédito Morada
_LINEA_POR_TIPO: dict[int, LineaCredito] = {
    2: LineaCredito.TDC,     # Tarjetas de crédito
    3: LineaCredito.ROT,     # Cartera bancaria rotativa
    48: LineaCredito.ROT,    # Sobregiro
    13: LineaCredito.VIV,    # Ahorro y vivienda
    15: LineaCredito.VIV,    # Construcción
    16: LineaCredito.VIV,    # Finca raíz
    23: LineaCredito.SOSTENIMIENTO,  # Telefonía celular
    24: LineaCredito.SOSTENIMIENTO,  # Comunicaciones
    29: LineaCredito.SOSTENIMIENTO,  # Servicios públicos
    43: LineaCredito.SOSTENIMIENTO,  # Educación
}

# Leasing habitacional (subtipos de accountType 14) son VIV
_LEASING_VIV_SUBTIPOS = {"01", "02", "05"}


def clasificar_linea_credito(account_type: int, sub_account_type: str) -> LineaCredito:
    if account_type == 14 and sub_account_type in _LEASING_VIV_SUBTIPOS:
        return LineaCredito.VIV
    if account_type in _LINEA_POR_TIPO:
        return _LINEA_POR_TIPO[account_type]
    return LineaCredito.CAB


# --------------------------------------------------------------------------
# Modelos de la respuesta HDC+
# --------------------------------------------------------------------------

class PersonId(BaseModel):
    personIdNumber: Optional[int] = None
    personIdType: Optional[int] = None
    personIdDesc: Optional[str] = None


class ProductResult(BaseModel):
    securityCode: Optional[str] = None
    consultDate: Optional[str] = None
    responseCode: int
    responseDesc: Optional[str] = None


class IdentifyingAttributes(BaseModel):
    personId: Optional[PersonId] = None
    personLastName: Optional[str] = None
    tradeholderIndicator: Optional[bool] = None


class BasicInformation(BaseModel):
    personId: Optional[PersonId] = None
    gender: Optional[int] = None
    names: Optional[str] = None
    firstLastName: Optional[str] = None
    secondLastName: Optional[str] = None
    fullName: Optional[str] = None
    citizenTaxRegistrationIndicator: Optional[bool] = None
    officialSourceValidationStatus: Optional[bool] = None


class AccountDetail(BaseModel):
    primaryKey: Optional[str] = None
    block: Optional[bool] = None
    rating: Optional[int] = None
    ratingDesc: Optional[str] = None
    filingCityName: Optional[str] = None
    filingCityCode: Optional[str] = None
    counterpartyIdNumber: Optional[str] = None
    businessLineName: Optional[str] = None
    accountOpeningDate: Optional[str] = None
    tradeHolderIndicator: Optional[str] = None
    accountNumber: Optional[int] = None
    filingOffice: Optional[str] = None
    economicSector: Optional[int] = None
    economicSectorName: Optional[str] = None
    stateOfAccountHolder: Optional[int] = None
    stateOfAccountHolderDesc: Optional[str] = None
    personId: Optional[PersonId] = None
    subAccountTypeName: Optional[str] = None
    accountType: Optional[int] = None
    subAccountType: Optional[str] = None
    subAccountTypeDesc: Optional[str] = None
    # Campos de crédito
    disbursementAmount: Optional[float] = None
    currentBalance: Optional[float] = None
    installmentAmount: Optional[float] = None
    creditLimit: Optional[float] = None
    pastDueAmount: Optional[float] = None
    pastDueInstallments: Optional[int] = None
    remainingInstallments: Optional[int] = None
    totalInstallments: Optional[int] = None
    accountExpirationDate: Optional[str] = None
    lastPaymentDate: Optional[str] = None
    behaviourDate: Optional[str] = None
    paymentPeriodicity: Optional[int] = None
    guarantorCode: Optional[str] = None


class AccountFeatures(BaseModel):
    accountCategory: Optional[int] = None
    accountCategoryDesc: Optional[str] = None


class AccountStatus(BaseModel):
    businessBureauEvent: Optional[str] = None
    businessBureauEventDesc: Optional[str] = None
    behaviourDate: Optional[str] = None


class AccountEntry(BaseModel):
    account: AccountDetail
    features: Optional[AccountFeatures] = None
    status: Optional[AccountStatus] = None


class InquiryFootprint(BaseModel):
    primaryKey: Optional[str] = None
    quantity: Optional[str] = None
    economicSectorName: Optional[str] = None
    economicSector: Optional[int] = None
    accountTypeName: Optional[str] = None
    filingOffice: Optional[str] = None
    filingCityName: Optional[str] = None
    inquiryBusinessName: Optional[str] = None
    counterpartyIdNumber: Optional[str] = None
    inquiryDate: Optional[str] = None
    inquiryReasonCode: Optional[str] = None


class ScoreModel(BaseModel):
    ScoreReason: Optional[List[str]] = None
    modelCode: Optional[Union[str, int]] = None
    modelCodeDesc: Optional[str] = None
    modelName: Optional[list] = None
    modelDate: Optional[str] = None
    scoreValue: Optional[int] = None
    population: Optional[int] = None


class ReportHDCplus(BaseModel):
    productResult: ProductResult
    identifyingAttributes: Optional[IdentifyingAttributes] = None
    basicInformation: Optional[BasicInformation] = None
    savings: List[AccountEntry] = []
    inquiryFootprints: List[InquiryFootprint] = []
    models: List[ScoreModel] = []


class HDCplusResponse(BaseModel):
    ReportHDCplus: ReportHDCplus


# --------------------------------------------------------------------------
# Modelo procesado para uso interno en Morada
# --------------------------------------------------------------------------

class ObligacionCredito(BaseModel):
    entidad_nit: str
    entidad_nombre: str
    linea_credito: LineaCredito
    account_type: int
    sub_account_type: str
    sub_account_type_desc: str = ""
    cupo: float = 0
    saldo: float = 0
    cuota_reportada: float = 0
    fecha_apertura: Optional[str] = None
    fecha_vencimiento: Optional[str] = None
    fecha_corte: Optional[str] = None
    calidad_deudor: str = "00"
    periodicidad: int = 1
    cuotas_restantes: Optional[int] = None
    cuotas_mora: int = 0
    monto_mora: float = 0


class ScoreExperian(BaseModel):
    model_code: str
    score_value: int
    model_date: Optional[str] = None


class ResultadoHDC(BaseModel):
    cedula: str
    nombre_completo: str = ""
    obligaciones: List[ObligacionCredito] = []
    scores: List[ScoreExperian] = []
    huellas_consulta: int = 0
    fecha_consulta: Optional[str] = None
    codigo_respuesta: int = 0
    mensaje_respuesta: str = ""

    @property
    def score_advance(self) -> Optional[int]:
        for s in self.scores:
            if s.model_code == "Z0":
                return s.score_value
        return None
