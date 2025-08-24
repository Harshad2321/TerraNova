import os
import shutil

def save_file(upload_dir: str, file_obj, filename: str) -> str:
    os.makedirs(upload_dir, exist_ok=True)
    path = os.path.join(upload_dir, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file_obj, buffer)
    return path
