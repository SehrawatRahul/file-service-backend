# app/core/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import requests

KEYCLOAK_REALM = "file-service"
KEYCLOAK_URL = "http://localhost:8080"
CLIENT_ID = "file-service-api"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

JWKS_URL = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"

# Fetch JWKS once and reuse
JWKS = requests.get(JWKS_URL).json()


def get_public_key(token):
    try:
        headers = jwt.get_unverified_header(token)
        kid = headers["kid"]

        for key in JWKS["keys"]:
            if key["kid"] == kid:
                return key

        raise Exception("Public key not found for given kid")

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        key = get_public_key(token)

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            options={"verify_aud": False},
            issuer=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}"
        )
        return payload

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid or expired token: {str(e)}"
        )
