from pydantic import BaseModel
from typing import Optional, List


class Vehicle_TypeBase(BaseModel):
    vehicle_type_id: Optional[int]
    log_id: str
    vehicle_type: Optional[str]

    def to_dict(self):
        return {
            "Vehicle Type Id": self.vehicle_type_id,
            "Log Id": self.log_id,
            "Vehicle Type": self.vehicle_type,
        }

    class Config:
        from_attributes = True


class Vehicle_TypeBaseResponse(BaseModel):
    status_id: int
    data: Optional[Vehicle_TypeBase] = None


class Vehicle_TypeBaseListResponse(BaseModel):
    status_id: int
    data: List[Vehicle_TypeBase] = []