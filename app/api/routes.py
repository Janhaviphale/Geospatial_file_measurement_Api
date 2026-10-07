import json
import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.config import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE,
    STORAGE_DIR,
)
from app.db.database import get_db
from app.models.file_record import FileRecord
from app.schemas.file_schema import (
    FileInfoResponse,
    MeasurementsResponse,
)
from app.services.file_processor import read_geospatial_file
from app.services.measurement import calculate_measurements


router = APIRouter(
    prefix="/api/files",
    tags=["Geospatial Files"],
)


def get_extension(filename: str) -> str:

    return Path(filename).suffix.lower()


@router.post(
    "/",
    response_model=FileInfoResponse,
    status_code=201,
)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    extension = get_extension(file.filename)

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Only .kml and .zip files are allowed."
            ),
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 50 MB limit.",
        )

    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_id = str(uuid.uuid4())

    safe_filename = Path(file.filename).name

    saved_path = STORAGE_DIR / f"{file_id}_{safe_filename}"

    saved_path.write_bytes(content)

    try:

        gdf = read_geospatial_file(saved_path)

        result = calculate_measurements(gdf)

        record = FileRecord(
            id=file_id,
            filename=safe_filename,
            file_type=extension,
            feature_count=len(gdf),
            crs=result["source_crs"],
            measurement_crs=result["measurement_crs"],
            status="COMPLETED",
            features_json=json.dumps(
                result["features"]
            ),
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return FileInfoResponse(
            id=record.id,
            filename=record.filename,
            feature_count=record.feature_count,
            crs=record.crs,
            measurement_crs=record.measurement_crs,
            status=record.status,
        )

    except ValueError as exc:

        if saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        if saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file: {str(exc)}",
        )

    finally:

        if saved_path.exists():
            saved_path.unlink()


@router.get(
    "/{file_id}/",
    response_model=FileInfoResponse,
)
def get_file_info(
    file_id: str,
    db: Session = Depends(get_db),
):

    record = (
        db.query(FileRecord)
        .filter(FileRecord.id == file_id)
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    return FileInfoResponse(
        id=record.id,
        filename=record.filename,
        feature_count=record.feature_count,
        crs=record.crs,
        measurement_crs=record.measurement_crs,
        status=record.status,
    )


@router.get(
    "/{file_id}/measurements/",
    response_model=MeasurementsResponse,
)
def get_measurements(
    file_id: str,
    db: Session = Depends(get_db),
):

    record = (
        db.query(FileRecord)
        .filter(FileRecord.id == file_id)
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    features = json.loads(
        record.features_json
    )

    return MeasurementsResponse(
        file_id=record.id,
        filename=record.filename,
        source_crs=record.crs,
        measurement_crs=record.measurement_crs,
        features=features,
    )