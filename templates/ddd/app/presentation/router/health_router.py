from fastapi import APIRouter
from pydantic import BaseModel

from app.shared.response.api_response import ApiResponse

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str


@router.get("/health", response_model=ApiResponse[HealthResponse])
async def get_health() -> ApiResponse[HealthResponse]:
    return ApiResponse.success(HealthResponse(status="ok"))
