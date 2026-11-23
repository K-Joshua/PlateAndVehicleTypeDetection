from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..Schema import Vehicle_PlateBase, Vehicle_TypeBase
from ..Dto.VehicleResponseDTO import VehicleLogResponseDTO
from ..db import get_db


router = APIRouter(
    prefix="/vehicle",
    tags=["Vehicle"]
)


@router.get(
    "/merge/{log_id}",
    response_model=VehicleLogResponseDTO
)
def merge_vehicle_data(
    log_id: str,
    session: Session = Depends(get_db)
):
    plate = session.exec(
        select(Vehicle_PlateBase)
        .where(Vehicle_PlateBase.log_id == log_id)
    ).first()

    vehicle_type = session.exec(
        select(Vehicle_TypeBase)
        .where(Vehicle_TypeBase.log_id == log_id)
    ).first()

    if not plate or not vehicle_type:
        raise HTTPException(
            status_code=404,
            detail="Vehicle data is incomplete"
        )

    return VehicleLogResponseDTO(
        log_id=log_id,
        vehicle_plate=plate.vehicle_plate,
        vehicle_type=vehicle_type.vehicle_type
    )