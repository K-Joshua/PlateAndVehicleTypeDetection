from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List
from datetime import datetime,timezone
from sqlalchemy import LargeBinary


# ---- USER TABLE
class Vehicle_Type(SQLModel, table = True):
    vehicle_type_id : Optional[int] = Field(default = None, primary_key= True, nullable=False, index= True)
    vehicle_type : str = Field(nullable=True, max_length=100)

class Vehicle_Plate(SQLModel, table = True):
    vehicle_plate_id : Optional[int] = Field(default = None, primary_key= True, nullable=False, index= True)
    vehicle_plate : str = Field(nullable=True, max_length=100)
    isEntry : bool = Field(nullable=True)
    
class vehicle_module(SQLModel, table = True):
    vehicle_id:Optional[int] = Field(default = None, primary_key= True, nullable=False, index= True)
    vehicle_img : str = Field(nullable=False)
    
class image_module(SQLModel, table=True):
    image_id: Optional[int] = Field(default=None, primary_key=True, nullable=False, index=True)
    image_data: bytes = Field(sa_type=LargeBinary, nullable=False)

class gate_module(SQLModel, table=True):
    gate_id: Optional[int] = Field(default=None, primary_key=True, nullable=False, index=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    should_open: bool = Field(default=False, nullable=False)