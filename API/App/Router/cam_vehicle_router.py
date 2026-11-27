
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import LargeBinary

from ..db import get_db
from ..model import image_module

router = APIRouter(prefix="/Image", tags=["Image"])

# POST - Save JPEG image
@router.post("/upload")
async def upload_image(
    image: UploadFile = File(...),
    session: Session = Depends(get_db)
):
    if image.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Only JPEG images are allowed")

    image_data = await image.read()

    if not image_data:
        raise HTTPException(status_code=400, detail="Image is empty")

    new_image = image_module(image_data=image_data)

    session.add(new_image)
    session.commit()
    session.refresh(new_image)

    return {
        "message": "Image uploaded successfully",
        "image_id": new_image.image_id
    }


# GET - Retrieve image
@router.get("/{image_id}")
def get_image(
    image_id: int,
    session: Session = Depends(get_db)
):
    image = session.get(image_module, image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return {
        "image_id": image.image_id,
        "image_data": image.image_data.hex()
    }
