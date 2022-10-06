import logging
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    BACKEND_CORS_ORIGIN_REGEX: Optional[str] = None

    class Config:
        case_sensitive = True


if os.path.isdir('/secrets'):
    settings = Settings(_secrets_dir="/secrets")
else:
    settings = Settings()
