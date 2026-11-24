from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..model import vehicle_module
from ..db import get_db

router = APIRouter(prefix="/vehicle", tags=["Vehicle"])


# POST - Save image string
@router.post("/image")
def save_vehicle_image(
    img_str: str,
    session: Session = Depends(get_db)
):
    vehicle = vehicle_module(vehicle_img=img_str)

    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)

    return {
        "message": "Vehicle image saved successfully",
        "vehicle_id": vehicle.vehicle_id,
        "vehicle_img": vehicle.vehicle_img
    }


# GET - Get all images
@router.get("/images")
def get_all_vehicle_images(
    session: Session = Depends(get_db)
):
    vehicles = session.exec(
        select(vehicle_module)
    ).all()

    return vehicles


# GET - Get latest image
@router.get("/image/latest")
def get_latest_vehicle_image(
    session: Session = Depends(get_session)
):
    vehicle = session.exec(
        select(vehicle_module)
        .order_by(vehicle_module.vehicle_id.desc())
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="No vehicle images found"
        )

    return vehicle