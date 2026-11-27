from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_db
from ..model import gate_module

router = APIRouter(prefix="/Gate", tags=["Gate"])


# POST - Save gate command
@router.post("/command")
def save_gate_command(
    should_open: bool,
    session: Session = Depends(get_db)
):
    new_gate = gate_module(should_open=should_open)

    session.add(new_gate)
    session.commit()
    session.refresh(new_gate)

    return {
        "message": "Gate command saved successfully",
        "gate_id": new_gate.gate_id,
        "timestamp": new_gate.timestamp,
        "should_open": new_gate.should_open
    }


# GET - Retrieve latest gate command
@router.get("/latest")
def get_latest_gate_command(
    session: Session = Depends(get_db)
):
    statement = select(gate_module).order_by(gate_module.gate_id.desc()).limit(1)
    gate = session.exec(statement).first()

    if not gate:
        raise HTTPException(status_code=404, detail="No gate commands found")

    return {
        "gate_id": gate.gate_id,
        "timestamp": gate.timestamp,
        "should_open": gate.should_open
    }