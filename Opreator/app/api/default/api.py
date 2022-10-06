from fastapi import APIRouter

from app.api.default.endpoints import chart

api_router = APIRouter()
api_router.include_router(chart.router, prefix="/charts", tags=["Charts"])

