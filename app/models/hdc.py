from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator
from typing import Any, List, Optional, Union
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
    22: LineaCredito.SOSTENIMIENTO,  # Celular
    23: LineaCredito.SOSTENIMIENTO,  # Telefonía celular
    24: LineaCredito.SOSTENIMIENTO,  # Comunicaciones
    29: LineaCredito.SOSTENIMIENTO,  # Servicios públicos
    43: LineaCredito.SOSTENIMIENTO,  # Educación
}

# Leasing habitacional (subtipos de accountType 14) son VIV
_LEASING_VIV_SUBTIPOS = {"01", "02", "05"}

# Tipos de cuenta que NO son obligaciones de crédito (ahorro / corriente)
TIPOS_CUENTA_NO_CREDITO = {1, 51}

# Estados de cuenta (status.account.businessAccountStatus) que indican
# obligación cerrada: no reportó, pago total, cancelada voluntariamente,
# cancelada por la entidad.
ESTADOS_CUENTA_CERRADA = {"00", "03", "08", "11"}


def clasificar_linea_credito(account_type: int, sub_account_type: str) -> LineaCredito:
    if account_type == 14 and sub_account_type in _LEASING_VIV_SUBTIPOS:
        return LineaCredito.VIV
    if account_type in _LINEA_POR_TIPO:
        return _LINEA_POR_TIPO[account_type]
    return LineaCredito.CAB


def _to_int(v: Any) -> Optional[int]:
    """Experian envía códigos a veces como int (11) y a veces como str ("05")."""
    if v is None or v == "":
        return None
    try:
        return int(str(v).strip())
    except (ValueError, TypeError):
        return None


def _to_code(v: Any, width: int = 2) -> Optional[str]:
    """Normaliza códigos a string con ceros a la izquierda ("00", "01", "96")."""
    if v is None or v == "":
        return None
    s = str(v).strip()
    return s.zfill(width) if s.isdigit() else s


def _to_float(v: Any) -> Optional[float]:
    if v is None or v == "":
        return None
    try:
        return float(str(v).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def _to_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    return str(v).strip()


# NOTA: Experian HDC+ no es consistente en los tipos: el mismo campo llega
# como int en una cuenta y como str en otra ("05" / 11, 16 / "01", "Q").
# Por eso los campos descriptivos que no intervienen en el cálculo se
# declaran `Any` y los que sí se usan tienen validadores de coerción.

# --------------------------------------------------------------------------
# Modelos de la respuesta HDC+
# --------------------------------------------------------------------------

class PersonId(BaseModel):
    model_config = ConfigDict(extra="allow")

    personIdNumber: Any = None
    personIdType: Any = None
    personIdDesc: Any = None


class ProductResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    securityCode: Any = None
    consultDate: Optional[str] = None
    responseCode: int
    responseDesc: Optional[str] = None

    @field_validator("responseCode", mode="before")
    @classmethod
    def _norm_response_code(cls, v):
        return _to_int(v)

    @field_validator("consultDate", "responseDesc", mode="before")
    @classmethod
    def _norm_str(cls, v):
        return _to_str(v)


class IdentifyingAttributes(BaseModel):
    model_config = ConfigDict(extra="allow")

    personId: Optional[PersonId] = None
    personLastName: Any = None
    tradeholderIndicator: Any = None


class BasicInformation(BaseModel):
    model_config = ConfigDict(extra="allow")

    personId: Optional[PersonId] = None
    gender: Any = None
    names: Optional[str] = None
    firstLastName: Optional[str] = None
    secondLastName: Optional[str] = None
    fullName: Optional[str] = None
    citizenTaxRegistrationIndicator: Any = None
    officialSourceValidationStatus: Any = None

    @field_validator("names", "firstLastName", "secondLastName", "fullName", mode="before")
    @classmethod
    def _norm_str(cls, v):
        return _to_str(v)


class AccountDetail(BaseModel):
    """Bloque `account` común a savings / liabilities / creditCard."""
    model_config = ConfigDict(extra="allow")

    primaryKey: Any = None
    block: Any = None
    rating: Any = None
    ratingDesc: Any = None
    filingCityName: Any = None
    filingCityCode: Any = None
    counterpartyIdNumber: Any = None
    businessLineName: Optional[str] = None
    businessLineCode: Optional[str] = None
    accountOpeningDate: Optional[str] = None
    tradeHolderIndicator: Any = None
    accountNumber: Any = None
    filingOffice: Any = None
    economicSector: Any = None
    economicSectorName: Any = None
    stateOfAccountHolder: Any = None
    stateOfAccountHolderDesc: Any = None
    personId: Optional[PersonId] = None
    subAccountTypeName: Any = None
    accountType: Optional[int] = None
    accountTypeDesc: Optional[str] = None
    subAccountType: Optional[str] = None
    subAccountTypeDesc: Optional[str] = None

    @field_validator("accountType", mode="before")
    @classmethod
    def _norm_account_type(cls, v):
        return _to_int(v)

    @field_validator("subAccountType", mode="before")
    @classmethod
    def _norm_sub_account_type(cls, v):
        return _to_code(v)

    @field_validator(
        "businessLineName", "businessLineCode", "accountOpeningDate",
        "accountTypeDesc", "subAccountTypeDesc", mode="before",
    )
    @classmethod
    def _norm_str(cls, v):
        return _to_str(v)

    @property
    def nombre_entidad(self) -> str:
        return (self.businessLineName or self.businessLineCode or "").strip()


class AccountValues(BaseModel):
    """Elemento de `values[]`: valores financieros al último corte."""
    model_config = ConfigDict(extra="allow")

    rating: Any = None
    ratingDesc: Any = None
    behaviourDate: Optional[str] = None
    currencyType: Any = None
    currencyTypeDesc: Any = None
    valueMonthlyPayment: Optional[float] = None
    paidInstallments: Optional[int] = None
    totalNumberOfInstallments: Optional[int] = None
    installmentsOverdue: Optional[int] = None
    delinquencyMaturation: Any = None
    availableBalance: Optional[float] = None
    paymentDeadline: Any = None
    paymentDate: Any = None
    periodicityOfPayments: Optional[int] = None
    periodicityOfPaymentsDesc: Any = None
    businessValueBalanceOverdue: Optional[float] = None
    debtBalance: Optional[float] = None
    initialValue: Optional[float] = None

    @field_validator(
        "valueMonthlyPayment", "availableBalance", "businessValueBalanceOverdue",
        "debtBalance", "initialValue", mode="before",
    )
    @classmethod
    def _norm_float(cls, v):
        return _to_float(v)

    @field_validator(
        "paidInstallments", "totalNumberOfInstallments", "installmentsOverdue",
        "periodicityOfPayments", mode="before",
    )
    @classmethod
    def _norm_int(cls, v):
        return _to_int(v)

    @field_validator("behaviourDate", mode="before")
    @classmethod
    def _norm_str(cls, v):
        return _to_str(v)


class AccountFeatures(BaseModel):
    """`featuresLiabilities` / `FeaturesCreditCard` / `features` (savings)."""
    model_config = ConfigDict(extra="allow")

    accountCategory: Any = None
    accountCategoryDesc: Any = None
    typeOfCredit: Any = None
    typeOfCreditDesc: Any = None
    contractType: Any = None
    contractTypeDesc: Any = None
    contractTerm: Any = None
    guaranteeType: Any = None
    guaranteeTypeName: Any = None
    typeOfDebtor: Optional[str] = None
    typeOfDebtorDesc: Optional[str] = None
    franchiseName: Any = None

    @field_validator("typeOfDebtor", mode="before")
    @classmethod
    def _norm_debtor(cls, v):
        return _to_code(v)

    @field_validator("typeOfDebtorDesc", mode="before")
    @classmethod
    def _norm_str(cls, v):
        return _to_str(v)


class ProductAccount(BaseModel):
    """`liabilitiesAccount` / `creditCardAccount`."""
    model_config = ConfigDict(extra="allow")

    expiryDate: Optional[str] = None
    paymentType: Optional[int] = None
    paymentTypeDesc: Any = None
    businessBehaviourVectorProduct: Any = None
    probabilityOfDefault: Any = None
    ratingHD: Any = None

    @field_validator("paymentType", mode="before")
    @classmethod
    def _norm_payment_type(cls, v):
        return _to_int(v)

    @field_validator("expiryDate", mode="before")
    @classmethod
    def _norm_str(cls, v):
        return _to_str(v)


class AccountStatusAccount(BaseModel):
    model_config = ConfigDict(extra="allow")

    businessAccountStatus: Optional[str] = None
    businessAccountStatusDesc: Optional[str] = None
    accountStatusDate: Any = None

    @field_validator("businessAccountStatus", mode="before")
    @classmethod
    def _norm_status(cls, v):
        return _to_code(v)

    @field_validator("businessAccountStatusDesc", mode="before")
    @classmethod
    def _norm_str(cls, v):
        return _to_str(v)


class AccountStatusPayment(BaseModel):
    model_config = ConfigDict(extra="allow")

    businessBureauEvent: Any = None
    businessBureauEventDesc: Any = None
    paymentDate: Any = None
    paymentMonths: Any = None


class AccountStatus(BaseModel):
    """En savings el status es plano; en liabilities/creditCard es anidado."""
    model_config = ConfigDict(extra="allow")

    # Forma plana (savings)
    businessBureauEvent: Any = None
    businessBureauEventDesc: Any = None
    behaviourDate: Any = None
    # Forma anidada (liabilities / creditCard)
    account: Optional[AccountStatusAccount] = None
    payment: Optional[AccountStatusPayment] = None
    origin: Any = None
    card: Any = None


class AccountEntry(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    account: AccountDetail
    features: Optional[AccountFeatures] = None
    featuresLiabilities: Optional[AccountFeatures] = None
    featuresCreditCard: Optional[AccountFeatures] = Field(
        default=None, alias="FeaturesCreditCard"
    )
    liabilitiesAccount: Optional[ProductAccount] = None
    creditCardAccount: Optional[ProductAccount] = None
    status: Optional[AccountStatus] = None
    values: List[AccountValues] = []

    @property
    def caracteristicas(self) -> Optional[AccountFeatures]:
        return self.featuresLiabilities or self.featuresCreditCard or self.features

    @property
    def producto(self) -> Optional[ProductAccount]:
        return self.liabilitiesAccount or self.creditCardAccount

    @property
    def valores(self) -> Optional[AccountValues]:
        return self.values[0] if self.values else None

    @property
    def estado_cuenta(self) -> Optional[str]:
        if self.status and self.status.account:
            return self.status.account.businessAccountStatus
        return None

    @property
    def estado_cuenta_desc(self) -> str:
        if self.status and self.status.account:
            return self.status.account.businessAccountStatusDesc or ""
        return ""

    @property
    def es_vigente(self) -> bool:
        """Obligación abierta: estado no cerrado y tipo de pago 0 (VIGENTE)."""
        if self.estado_cuenta in ESTADOS_CUENTA_CERRADA:
            return False
        prod = self.producto
        if prod is not None and prod.paymentType not in (None, 0):
            return False
        return True


class InquiryFootprint(BaseModel):
    model_config = ConfigDict(extra="allow")

    primaryKey: Any = None
    quantity: Any = None
    economicSectorName: Any = None
    economicSector: Any = None
    accountTypeName: Any = None
    accountTypeDesc: Any = None
    filingOffice: Any = None
    filingCityName: Any = None
    inquiryBusinessName: Any = None
    counterpartyIdNumber: Any = None
    inquiryDate: Any = None
    inquiryReasonCode: Any = None


class ScoreModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    ScoreReason: Any = None
    modelCode: Optional[str] = None
    modelCodeDesc: Any = None
    modelName: Any = None
    modelDate: Optional[str] = None
    scoreValue: Optional[int] = None
    population: Any = None

    @field_validator("scoreValue", mode="before")
    @classmethod
    def _norm_score(cls, v):
        return _to_int(v)

    @field_validator("modelCode", "modelDate", mode="before")
    @classmethod
    def _norm_str(cls, v):
        return _to_str(v)


class ReportHDCplus(BaseModel):
    model_config = ConfigDict(extra="allow")

    productResult: ProductResult
    identifyingAttributes: Optional[IdentifyingAttributes] = None
    basicInformation: Optional[BasicInformation] = None
    savings: List[AccountEntry] = []
    liabilities: List[AccountEntry] = []
    creditCard: List[AccountEntry] = []
    location: Any = None
    globalIndebtedness: Any = None
    inquiryFootprints: List[InquiryFootprint] = []
    models: List[ScoreModel] = []
    agregatedInfo: Any = None
    agregatedInfoMicrocredit: Any = None

    @field_validator(
        "savings", "liabilities", "creditCard", "inquiryFootprints", "models",
        mode="before",
    )
    @classmethod
    def _none_a_lista(cls, v):
        """Experian puede omitir la sección o enviarla como null."""
        if v is None:
            return []
        if isinstance(v, dict):
            return [v]
        return v


class HDCplusResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

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
    calidad_deudor_desc: str = ""
    periodicidad: int = 1
    cuotas_restantes: Optional[int] = None
    cuotas_pagadas: Optional[int] = None
    total_cuotas: Optional[int] = None
    cuotas_mora: int = 0
    monto_mora: float = 0
    estado_cuenta: str = ""
    estado_cuenta_desc: str = ""
    vigente: bool = True


class ScoreExperian(BaseModel):
    model_code: str
    score_value: int
    model_date: Optional[str] = None


# Códigos de modelo de score en orden de preferencia
_MODELOS_SCORE_PREFERIDOS = ("Z0", "DF")


class ResultadoHDC(BaseModel):
    cedula: str
    nombre_completo: str = ""
    obligaciones: List[ObligacionCredito] = []
    obligaciones_cerradas: int = 0
    scores: List[ScoreExperian] = []
    huellas_consulta: int = 0
    fecha_consulta: Optional[str] = None
    codigo_respuesta: int = 0
    mensaje_respuesta: str = ""
    # Respuesta cruda de Experian, tal como llegó (para "Ver JSON original")
    respuesta_original: Optional[dict] = None

    @computed_field  # type: ignore[misc]
    @property
    def score_advance(self) -> Optional[int]:
        """Score del solicitante. Preferencia Z0 > DF > cualquier otro.
        Un score de 0 significa "sin score" y se devuelve None."""
        por_codigo = {s.model_code: s.score_value for s in self.scores}
        for code in _MODELOS_SCORE_PREFERIDOS:
            if por_codigo.get(code):
                return por_codigo[code]
        for s in self.scores:
            if s.score_value:
                return s.score_value
        return None
