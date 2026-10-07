from typing import Any, Optional

from pydantic import BaseModel


class FileInfoResponse(BaseModel):
    id: str
    filename: str
    feature_count: int
    crs: Optional[str] = None
    measurement_crs: Optional[str] = None
    status: str


class FeatureMeasurement(BaseModel):
    feature_id: int
    geometry_type: str
    geometry: dict[str, Any]
    properties: dict[str, Any]
    area_m2: Optional[float] = None
    length_m: Optional[float] = None


class MeasurementsResponse(BaseModel):
    file_id: str
    filename: str
    source_crs: Optional[str] = None
    measurement_crs: Optional[str] = None
    features: list[FeatureMeasurement]