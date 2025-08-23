from fastapi import APIRouter, UploadFile, File
from PIL import Image
import os

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_DIR = "uploaded_maps"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/map")
async def upload_map(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Open with Pillow
        with open(file_path, "wb") as f:
            f.write(contents)

        img = Image.open(file_path)

        # 🔴 FIX: Convert RGBA → RGB (removes alpha channel)
        if img.mode == "RGBA":
            img = img.convert("RGB")

        processed_path = os.path.join(UPLOAD_DIR, "processed_" + file.filename.replace(" ", "_") + ".jpg")
        img.save(processed_path, "JPEG")

        return {
            "message": "Map uploaded and processed successfully",
            "processed_path": processed_path
        }
    except Exception as e:
        return {"error": str(e)}
