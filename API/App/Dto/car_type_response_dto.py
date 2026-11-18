from pydantic import BaseModel
from typing import List, Optional


class VehicleDataDTO(BaseModel):
    vehicle_type: str
    confidence: float
    coordinates: List[float]


class VehicleResponseDTO(BaseModel):
    request_status: str
    status_code: int
    message: Optional[str] = None
    data: List[VehicleDataDTO]