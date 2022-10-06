from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Body

from app.services.pods_service import create_instance, edit_instance, delete_instance
from pydantic import BaseModel

router = APIRouter()

@router.post(
    "/create_crd",
    # response_model=List[schemas.],
)
async def create(
        body: BaseModel,
        request: Request
) -> Any:
    try:
        webhook_body = await request.json()
    except Exception as err:
        # could not parse json
        webhook_body = await request.body()

    print(webhook_body)

    create_instance(webhook_body)

    """
    create instance.
    """
    return 200

@router.post(
    "/edit_crd",
    # response_model=List[schemas.],
)
async def edit(
        body: BaseModel,
        request: Request
) -> Any:
    try:
        webhook_body = await request.json()
    except Exception as err:
        # could not parse json
        webhook_body = await request.body()

    edit_instance(webhook_body)

    """
    edit instance.
    """
    return 200


@router.post(
    "/delete_crd",
    # response_model=List[schemas.],
)
async def edit(
        branch,
) -> Any:

    delete_instance(branch)

    """
    delete instance.
    """
    return 200