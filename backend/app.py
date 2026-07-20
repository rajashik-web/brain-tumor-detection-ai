from fastapi import FastAPI

from backend.api.routes import router

app = FastAPI(
    title="Brain Tumor Detection API",
    description="Deep Learning API for MRI Brain Tumor Classification",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Brain Tumor Detection API is running"
    }