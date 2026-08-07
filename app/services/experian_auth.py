import time
import base64
from dataclasses import dataclass, field
from typing import Optional

import httpx

from app.config import settings


@dataclass
class _CachedToken:
    access_token: str
    expires_at: float


_token_hdc: Optional[_CachedToken] = None
_token_vi: Optional[_CachedToken] = None

_MARGIN_SECONDS = 60


async def obtener_token_hdc() -> str:
    global _token_hdc
    if _token_hdc and time.time() < _token_hdc.expires_at:
        return _token_hdc.access_token

    url = f"{settings.experian_base_url}/spla/oauth2/v1/token"
    headers = {
        "Content-Type": "application/json",
        "client_id": settings.EXPERIAN_CLIENT_ID,
        "client_secret": settings.EXPERIAN_CLIENT_SECRET,
    }
    body = {
        "username": settings.EXPERIAN_OKTA_USERNAME,
        "password": settings.EXPERIAN_OKTA_PASSWORD,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json=body, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    expires_in = int(data.get("expires_in", 1800))
    _token_hdc = _CachedToken(
        access_token=data["access_token"],
        expires_at=time.time() + expires_in - _MARGIN_SECONDS,
    )
    return _token_hdc.access_token


async def obtener_token_valor_ingreso() -> str:
    global _token_vi
    if _token_vi and time.time() < _token_vi.expires_at:
        return _token_vi.access_token

    url = settings.EXPERIAN_VI_TOKEN_URL
    credentials = base64.b64encode(
        f"{settings.EXPERIAN_VI_CLIENT_ID}:{settings.EXPERIAN_VI_CLIENT_SECRET}".encode()
    ).decode()

    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {credentials}",
    }
    data = {
        "grant_type": "password",
        "username": settings.EXPERIAN_VI_OKTA_USERNAME,
        "password": settings.EXPERIAN_VI_OKTA_PASSWORD,
        "scope": "expco_incomes",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, data=data, headers=headers)
        resp.raise_for_status()
        result = resp.json()

    expires_in = int(result.get("expires_in", 3600))
    _token_vi = _CachedToken(
        access_token=result["access_token"],
        expires_at=time.time() + expires_in - _MARGIN_SECONDS,
    )
    return _token_vi.access_token
