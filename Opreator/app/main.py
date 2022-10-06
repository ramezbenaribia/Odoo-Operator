from datetime import datetime

from fastapi import FastAPI
from fastapi_extra.middleware.mutual_tls import MutualTLSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app import api_version

from app.api.default.api import api_router

from fastapi_extra.utils.customize_fastapi import customize_fastapi_responses
from ipomm_commons.runtime import fastapi_app
from ipomm_commons.utils import microservice_config

now = datetime.now()

sub_app = FastAPI(
    title=microservice_config.PROJECT_NAME + ' ' + now.strftime("%d/%m/%Y %H:%M:%S"),
    openapi_url=f"/openapi.json",
    docs_url=f"/docs", redoc_url=f"/redoc",
)

sub_app.add_middleware(GZipMiddleware, minimum_size=1000)
sub_app.add_middleware(MutualTLSMiddleware)


customize_fastapi_responses(sub_app)

sub_app.include_router(api_router, prefix="")

API_URL = microservice_config.API_URL_PREFIX + '/' + api_version
fastapi_app.mount(API_URL, sub_app)


app = fastapi_app
