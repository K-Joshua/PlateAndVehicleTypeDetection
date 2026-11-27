
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from .db import create_db_and_tables


from .Router import ocr_plate_detection_router, yolo_car_type_detection_route, find_same_logID_router, get_total_count_vehicle, vehicle_router, cam_vehicle_router


# from Router import ai_group_route
# from config import Setting # -- Remote 


from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    try: 
        create_db_and_tables()
        yield
    except Exception as e:
        print(f"Failed to create DB tables: {e}")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:4200"],  # Angular Focus ----  TEMPORARY MWEHEHEH
    allow_origins=["*"],  # Allows all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(ocr_plate_detection_router.plate)
app.include_router(yolo_car_type_detection_route.vehicle)
app.include_router(find_same_logID_router.router)
app.include_router(get_total_count_vehicle.statistics)
app.include_router(vehicle_router.router)
app.include_router(cam_vehicle_router.router)