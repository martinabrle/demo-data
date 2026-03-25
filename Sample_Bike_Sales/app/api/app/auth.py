"""Microsoft Entra ID (Azure AD) token validation with MSAL."""

from __future__ import annotations

import os
from typing import Optional

import jwt
import requests
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# ── configuration (set via env vars or .env) ─────────────────────────────────
TENANT_ID: str = os.getenv("AZURE_TENANT_ID", "")
CLIENT_ID: str = os.getenv("AZURE_CLIENT_ID", "")  # App registration client-id
AUDIENCE: str = os.getenv("AZURE_API_AUDIENCE", CLIENT_ID)  # typically api://<client-id>
ISSUER: str = f"https://login.microsoftonline.com/{TENANT_ID}/v2.0" if TENANT_ID else ""

_OIDC_CONFIG_URL = (
    f"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration"
    if TENANT_ID
    else ""
)

_jwks_client: Optional[jwt.PyJWKClient] = None

_bearer_scheme = HTTPBearer(auto_error=True)


def _get_jwks_client() -> jwt.PyJWKClient:
    """Lazily build and cache a PyJWKClient from the OIDC discovery endpoint."""
    global _jwks_client
    if _jwks_client is None:
        if not _OIDC_CONFIG_URL:
            raise HTTPException(
                status_code=500,
                detail="AZURE_TENANT_ID is not configured. Cannot validate tokens.",
            )
        oidc_config = requests.get(_OIDC_CONFIG_URL, timeout=10).json()
        jwks_uri = oidc_config["jwks_uri"]
        _jwks_client = jwt.PyJWKClient(jwks_uri)
    return _jwks_client


def _decode_token(token: str) -> dict:
    """Validate and decode a Bearer JWT issued by Entra ID."""
    client = _get_jwks_client()
    signing_key = client.get_signing_key_from_jwt(token)
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=AUDIENCE,
        issuer=ISSUER,
        options={"require": ["exp", "iss", "aud"]},
    )
    return payload


async def validate_token(request: Request) -> dict:
    """FastAPI dependency – extracts and validates the Bearer token.

    Returns the decoded JWT claims dict so downstream handlers can
    inspect scopes / roles / user info.
    """
    # ── bypass auth when Entra ID is not configured and it's local dev ───────
    if not TENANT_ID or not CLIENT_ID:
        if os.getenv("AZURE_EXTENSION_DIR") is not None:
            print("Running on Azure without Tenant ID and Client ID!")
            raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
        return {"note": "Auth disabled – AZURE_TENANT_ID / AZURE_CLIENT_ID not set"}

    credentials: HTTPAuthorizationCredentials = await _bearer_scheme(request)
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    try:
        claims = _decode_token(credentials.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidAudienceError:
        raise HTTPException(status_code=401, detail="Invalid audience")
    except jwt.InvalidIssuerError:
        raise HTTPException(status_code=401, detail="Invalid issuer")
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {exc}")

    return claims
