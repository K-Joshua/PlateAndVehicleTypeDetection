from pydantic import BaseModel


class VehicleLogResponseDTO(BaseModel):
    log_id: str
    vehicle_plate: str
    vehicle_type: str