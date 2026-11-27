from pydantic import BaseModel


class image_dto(BaseModel):
    message: str
    image_id: int