from pydantic import BaseModel
from typing import Optional, List


class Vehicle_PlateBase(BaseModel):
    vehicle_plate_id: Optional[int]
    log_id: str
    vehicle_plate: Optional[str]

    def to_dict(self):
        return {
            "Vehicle Plate Id": self.vehicle_plate_id,
            "Log Id": self.log_id,
            "Vehicle Plate": self.vehicle_plate,
        }

    class Config:
        from_attributes = True


class Vehicle_PlateBaseResponse(BaseModel):
    status_id: int
    data: Optional[Vehicle_PlateBase] = None


class Vehicle_PlateBaseListResponse(BaseModel):
    status_id: int
    data: List[Vehicle_PlateBase] = []