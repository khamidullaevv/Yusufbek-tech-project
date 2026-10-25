from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.calculator import calculate_estimate
from app.db import get_materials


router = APIRouter()


class CalculateRequest(BaseModel):
    area_sqm: float = Field(gt=0, le=1000)
    repair_type: Literal["Косметический", "Капитальный"]


@router.get("/materials")
def list_materials() -> dict:
    return {"materials": get_materials()}


@router.post("/calculate")
def calculate(request: CalculateRequest) -> dict:
    return calculate_estimate(
        request.area_sqm,
        request.repair_type,
        get_materials(),
    )
