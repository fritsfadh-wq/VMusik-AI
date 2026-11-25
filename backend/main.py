
import os
from pathlib import Path

import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="VMusic AI")

BASE_DIR = Path(__file__).resolve().parent.parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/health")
def health():
    return {
        "status": "online",
        "app": "VMusic AI",
        "generator": bool(os.getenv("YUE2_WORKER_URL")),
        "cover": bool(os.getenv("RVC_WORKER_URL"))
    }

@app.post("/generate")
async def generate(data: dict):
    worker = os.getenv("YUE2_WORKER_URL")

    if not worker:
        raise HTTPException(
            status_code=503,
            detail="AI Music Generator belum terhubung ke YuE2."
        )

    try:
        response = requests.post(worker, json=data, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        raise HTTPException(status_code=502, detail=str(error))

@app.post("/convert")
async def convert(audio: UploadFile = File(...)):
    worker = os.getenv("RVC_WORKER_URL")

    if not worker:
        raise HTTPException(
            status_code=503,
            detail="AI Cover belum terhubung ke RVC."
        )

    try:
        content = await audio.read()
        response = requests.post(
            worker,
            files={"audio": (
                audio.filename,
                content,
                audio.content_type
            )},
            timeout=300
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        raise HTTPException(status_code=502, detail=str(error))
        
