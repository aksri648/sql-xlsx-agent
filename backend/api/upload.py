from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import os
import uuid
import aiofiles
from typing import Optional

from backend.services.file_handler import FileHandler
from backend.vectorstore.chroma_manager import ChromaManager

router = APIRouter(prefix="/upload", tags=["upload"])
file_handler = FileHandler()
chroma_manager = ChromaManager()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/csv")
async def upload_csv(file: UploadFile = File(...), dataset_name: Optional[str] = None):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    dataset_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{dataset_id}.csv")

    content = await file.read()
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    try:
        df = file_handler.read_csv(file_path)
        schema = file_handler.get_schema(df)
        profile = file_handler.profile_dataset(df)

        chroma_manager.add_schema(
            schema_data=schema,
            metadata={
                "id": dataset_id,
                "name": dataset_name or file.filename,
                "type": "csv",
            }
        )

        return JSONResponse({
            "id": dataset_id,
            "name": dataset_name or file.filename,
            "source_type": "file",
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": schema["columns"],
            "schema": profile,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/excel")
async def upload_excel(file: UploadFile = File(...), dataset_name: Optional[str] = None, sheet_name: Optional[str] = None):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="File must be an Excel file")

    dataset_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{dataset_id}.xlsx")

    content = await file.read()
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    try:
        df = file_handler.read_excel(file_path, sheet_name)
        schema = file_handler.get_schema(df)
        profile = file_handler.profile_dataset(df)

        chroma_manager.add_schema(
            schema_data=schema,
            metadata={
                "id": dataset_id,
                "name": dataset_name or file.filename,
                "type": "excel",
            }
        )

        return JSONResponse({
            "id": dataset_id,
            "name": dataset_name or file.filename,
            "source_type": "file",
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": schema["columns"],
            "schema": profile,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))