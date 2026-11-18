from ultralytics import YOLO
from pathlib import Path


class generate_vehicle_detection:
    def detect_vehicle(image_path):

        MODEL_PATH = (Path(__file__).parent.parent/ "Models"/ "yolo11m.pt")

        model = YOLO(str(MODEL_PATH))

        results = model(
            str(image_path)
        )

        detected_vehicles = []

        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                coordinates = box.xyxy[0].tolist()

                class_name = result.names[class_id]

                print("Object:", class_name)
                print(f"Confidence: {100 * confidence:.2f}")
                print("Coordinates:", coordinates)
                print("-------------------")

                detected_vehicles.append({
                    "vehicle_type": class_name,
                    "confidence": confidence,
                    "coordinates": coordinates
                })

        return detected_vehicles