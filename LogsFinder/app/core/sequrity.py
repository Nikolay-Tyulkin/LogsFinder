from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from app.core.config import Settings

settings = Settings()

api_key_header = APIKeyHeader(name=settings.API_KEY_NAME)
api_key = settings.SECRET_KEY

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == api_key:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")