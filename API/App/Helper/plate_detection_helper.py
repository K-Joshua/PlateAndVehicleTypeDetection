import cv2
from ultralytics import YOLO
from pathlib import Path


class generate_plate_jpeg_after_detection:
    def crop_platenumber_N_save_crop_picture_to_assets(image_path):

        MODEL_PATH = Path(__file__).parent.parent / "Models" / "license-plate-finetune-v1n.pt"
        GEN_IMAGE_PATH = Path(__file__).parent.parent / "Assets" / "plate_crop.jpg"

        model = YOLO(str(MODEL_PATH))

        image = cv2.imread(str(image_path))

        if image is None:
            raise FileNotFoundError(
                f"Could not load image: {image_path}"
            )

        results = model.predict(
            source=image,
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

                plate = image[y1:y2, x1:x2]

                cv2.imwrite(
                    str(GEN_IMAGE_PATH),
                    plate
                )

                print(
                    "Saved: plate_crop.jpg"
                )

                return GEN_IMAGE_PATH

        return None