from fastapi import APIRouter , File , Depends, UploadFile
import shutil

from fastapi.responses import FileResponse

file_router = APIRouter()

@file_router.post("/upload")
async def file_uploader(file : UploadFile  = File(...)):
    path = f"backend/statics/files/{file.filename}"
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(file.file,buffer)
        
    return {
        "file_name" : file.filename,
        "file_size": f"{int(file.size/1024)} KB",
        "file_headers": file.headers,
        "file_content_type": file.content_type
    }

@file_router.get("/download/{name}", response_class=FileResponse)
async def file_downloader(name: str):
    path = f"statics/files/{name}"
    return path