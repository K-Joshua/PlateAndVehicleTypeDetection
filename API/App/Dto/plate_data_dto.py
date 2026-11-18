from pydantic import BaseModel

class PlateDataDTO(BaseModel):
    plate_number: str
    confidence: float


class PlateResponseDTO(BaseModel):
    request_status: str
    status_code: int
    data: PlateDataDTO