import cv2
import numpy as np

from ultralytics import YOLO
from pathlib import Path


class generate_plate_jpeg_after_detection:

    def crop_platenumber_N_save_crop_picture_to_assets(image):

        MODEL_PATH = (
            Path(__file__).parent.parent
            / "Models"
            / "license-plate-finetune-v1n.pt"
        )

        OUTPUT_PATH = (
            Path(__file__).parent.parent
            / "Assets"
            / "plate_crop.jpg"
        )

        model = YOLO(str(MODEL_PATH))

        image_data = image.file.read()

        image_array = cv2.imdecode(
            np.frombuffer(
                image_data,
                dtype=np.uint8
            ),
            cv2.IMREAD_COLOR
        )

        if image_array is None:
            raise FileNotFoundError(
                "Could not decode uploaded image."
            )

        results = model.predict(
            source=image_array,
            conf=0.25
        )

        for result in results:

            for box in result.boxes:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist()
                )

                confidence = float(box.conf[0])

                print(
                    f"License Plate Confidence: {confidence:.2%}"
                )

                print(
                    f"Coordinates: ({x1}, {y1}) -> ({x2}, {y2})"
                )

                plate = image_array[y1:y2, x1:x2]

                cv2.imwrite(
                    str(OUTPUT_PATH),
                    plate
                )

                print(
                    f"Saved: {OUTPUT_PATH}"
                )

                return OUTPUT_PATH

        return None 