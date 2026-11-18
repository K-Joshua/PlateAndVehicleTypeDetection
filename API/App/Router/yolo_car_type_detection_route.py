import logging
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from Dto import car_type_response_dto
from Helper import yolo_vehicle_type_helper as gen_vehicle


logger = logging.getLogger(__name__)


vehicle = APIRouter(prefix="/Vehicle",tags=["Vehicle Detection"])


@vehicle.post("/detect",response_model=car_type_response_dto.VehicleResponseDTO)
async def detect_vehicle(image: UploadFile = File(...)):
    temporary_image_path = None

    try:
        logger.info("Vehicle detection started: %s",image.filename)

        suffix = Path(image.filename or ".jpg").suffix

        with tempfile.NamedTemporaryFile(delete=False,suffix=suffix) as temp_image:

            temporary_image_path = Path(
                temp_image.name
            )

            image_data = await image.read()

            temp_image.write(image_data)

        detected_vehicles = (gen_vehicle.generate_vehicle_detection.detect_vehicle(temporary_image_path))

        if not detected_vehicles:
            raise HTTPException(
                status_code=404,
                detail="No vehicle was detected."
            )

        if len(detected_vehicles) > 1:
            logger.warning(
                "Multiple vehicles detected: %s vehicles.",
                len(detected_vehicles)
            )

            return car_type_response_dto.VehicleResponseDTO(
                request_status="warning",
                status_code=200,
                message="Multiple vehicles detected.",
                data=detected_vehicles
            )

        logger.info(
            "Vehicle detection completed."
        )

        return car_type_response_dto.VehicleResponseDTO(
            request_status="success",
            status_code=200,
            data=detected_vehicles
        )

    except HTTPException:
        raise

    except Exception as exc:

        logger.exception(
            "Vehicle detection failed."
        )

        raise HTTPException(
            status_code=500,
            detail=f"Vehicle detection failed: {exc}"
        )

    finally:

        if temporary_image_path:

            try:
                temporary_image_path.unlink(
                    missing_ok=True
                )

            except Exception:

                logger.exception(
                    "Failed to delete temporary image."
                )