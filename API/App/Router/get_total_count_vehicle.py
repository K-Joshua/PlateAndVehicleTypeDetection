from datetime import datetime, time

from fastapi import APIRouter
from sqlmodel import Session, select

from ..db import engine
from ..model import Vehicle_Plate

statistics = APIRouter(
    prefix="/Statistics",
    tags=["Vehicle Statistics"]
)


@statistics.get("/total-today")
def get_total_vehicle_today():

    today = datetime.now().date()

    start_of_day = datetime.combine(
        today,
        time.min
    )

    end_of_day = datetime.combine(
        today,
        time.max
    )

    with Session(engine) as session:

        statement = select(Vehicle_Plate).where(
            Vehicle_Plate.is_entry == True,
            Vehicle_Plate.timestamp >= start_of_day,
            Vehicle_Plate.timestamp <= end_of_day
        )

        vehicles = session.exec(statement).all()

    return {
        "request_status": "success",
        "status_code": 200,
        "total_vehicle": len(vehicles)
    }