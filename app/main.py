from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base, engine
from app.models.file_record import FileRecord


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Geospatial File Measurement API",
    description=(
        "API for uploading KML and Shapefile ZIP files, "
        "extracting geospatial features, and calculating "
        "area and length measurements."
    ),
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "message": "Geospatial File Measurement API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }