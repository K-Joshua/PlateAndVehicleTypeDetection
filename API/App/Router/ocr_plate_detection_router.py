import logging
import re
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from paddleocr import PaddleOCR

from Helper import plate_detection_helper as gen_plate_num
from Helper import delete_picture_helper as del_picture
from Dto import plate_data_dto

logger = logging.getLogger(__name__)


PLATE_PATTERNS = [
    r"^[A-Z]{3}[0-9]{4}$",
    r"^[0-9]{3}[A-Z]{3}$",
    r"^[A-Z][0-9]{3}[A-Z]{2}$",
    r"^[A-Z]{2}[0-9]{5}$",
]

ocr = PaddleOCR(use_textline_orientation=True,lang="en",enable_mkldnn=False)

plate = APIRouter(prefix="/Plate",tags=["License Plate Recognition"])

def is_valid_plate(text: str):
    text = text.upper().replace(" ", "").strip()

    return any(
        re.fullmatch(pattern, text)
        for pattern in PLATE_PATTERNS
    )


@plate.post("/read", response_model=plate_data_dto.PlateResponseDTO)
async def read_license_plate(
    image: UploadFile = File(...)
):
    plate_image_path = None
    temporary_image_path = None

    try:
        logger.info(
            "License plate recognition started: %s",
            image.filename
        )

        suffix = Path(image.filename or ".jpg").suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_image:

            temporary_image_path = Path(temp_image.name)

            image_data = await image.read()

            temp_image.write(image_data)

        logger.info(
            "Uploaded image saved: %s",
            temporary_image_path
        )

        plate_image_path = (gen_plate_num.generate_plate_jpeg_after_detection.crop_platenumber_N_save_crop_picture_to_assets(temporary_image_path)
        )

        if plate_image_path is None:
            raise HTTPException(
                status_code=404,
                detail="License plate was not detected."
            )

        logger.info(
            "License plate detected."
        )

        results = ocr.predict(
            str(plate_image_path)
        )

        detected_plates = []

        for result in results:

            data = result.json["res"]

            for text, confidence in zip(
                data["rec_texts"],
                data["rec_scores"]
            ):

                extracted_text = (
                    text.upper()
                    .replace(" ", "")
                    .strip()
                )

                if is_valid_plate(extracted_text):

                    detected_plates.append({
                        "plate_number": extracted_text,
                        "confidence": float(confidence)
                    })

        if not detected_plates:
            raise HTTPException(
                status_code=422,
                detail="License plate was detected, but no valid plate number was recognized."
            )

        best_plate = max(
            detected_plates,
            key=lambda plate: plate["confidence"]
        )

        logger.info(
            "License plate recognized: %s",
            best_plate["plate_number"]
        )

        return plate_data_dto.PlateResponseDTO(
            request_status="success",
            status_code=200,
            data=plate_data_dto.PlateDataDTO(
                plate_number=best_plate["plate_number"],
                confidence=best_plate["confidence"]
            )
)

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(
            "License plate recognition failed."
        )

        raise HTTPException(
            status_code=500,
            detail=f"License plate recognition failed: {exc}"
        )

    finally:

        if temporary_image_path:
            try:
                temporary_image_path.unlink(
                    missing_ok=True
                )
            except Exception:
                logger.exception(
                    "Failed to delete temporary uploaded image."
                )

        if plate_image_path:
            try:
                del_picture.picture_helper.delete_jpeg_picture(
                    plate_image_path
                )
            except Exception:
                logger.exception(
                    "Failed to delete plate crop image."
                )