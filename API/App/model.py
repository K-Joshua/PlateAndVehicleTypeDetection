from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List
from datetime import datetime


# ---- USER TABLE
class Vehicle_Type(SQLModel, table = True):
    vehicle_type_id : Optional[int] = Field(default = None, primary_key= True, nullable=False, index= True)
    log_id : str = Field(nullable=False, max_length=200)
    vehicle_type : str = Field(nullable=True, max_length=100)

class Vehicle_Plate(SQLModel, table = True):
    vehicle_plate_id : Optional[int] = Field(default = None, primary_key= True, nullable=False, index= True)
    log_id : str = Field(nullable=False, max_length=200)
    vehicle_plate : str = Field(nullable=True, max_length=100)
    isEntry : bool = Field(nullable=True)
    
class vehicle_module(SQLModel, table = True):
    vehicle_id:Optional[int] = Field(default = None, primary_key= True, nullable=False, index= True)
    vehicle_img : str = Field(nullable=False)