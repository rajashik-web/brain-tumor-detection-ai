from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.inference.pipeline import InferencePipeline
from backend.schema.response import PredictionResponse
from backend.config import UPLOAD_DIR,MODEL_PATH


router = APIRouter()

pipeline = InferencePipeline()

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post(
    "/predict",
    response_model=PredictionResponse
)
async def predict(file: UploadFile = File(...)):

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image."
        )

    extension = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{extension}"
    image_path = UPLOAD_DIR / filename

    try:

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = pipeline.predict(str(image_path))

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

    finally:

        if image_path.exists():
            image_path.unlink()