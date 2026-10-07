import shutil
import tempfile
import zipfile
from pathlib import Path

import geopandas as gpd


def validate_zip_members(zip_file: zipfile.ZipFile):
    """
    Protect against ZIP path traversal attacks.
    """

    for member in zip_file.namelist():

        member_path = Path(member)

        if member_path.is_absolute():
            raise ValueError(
                "ZIP file contains an unsafe absolute path."
            )

        if ".." in member_path.parts:
            raise ValueError(
                "ZIP file contains an unsafe path."
            )


def extract_shapefile(zip_path: Path, destination: Path) -> Path:
    """
    Extract a ZIP file and locate the Shapefile.
    """

    with zipfile.ZipFile(zip_path, "r") as zip_ref:

        if zip_ref.testzip() is not None:
            raise ValueError("The ZIP file is corrupted.")

        validate_zip_members(zip_ref)

        zip_ref.extractall(destination)

    shapefiles = list(destination.rglob("*.shp"))

    if not shapefiles:
        raise ValueError(
            "ZIP file does not contain a Shapefile (.shp)."
        )

    if len(shapefiles) > 1:
        raise ValueError(
            "ZIP file contains multiple Shapefiles. "
            "Please upload one Shapefile per ZIP."
        )

    return shapefiles[0]


def read_geospatial_file(file_path: Path):

    extension = file_path.suffix.lower()

    temporary_directory = Path(
        tempfile.mkdtemp(prefix="geo_processing_")
    )

    try:

        if extension == ".kml":

            gdf = gpd.read_file(
                file_path,
                driver="KML",
                engine="fiona",
            )

        elif extension == ".zip":

            shapefile_path = extract_shapefile(
                file_path,
                temporary_directory,
            )

            gdf = gpd.read_file(
                shapefile_path,
                engine="fiona",
            )

        else:

            raise ValueError(
                "Unsupported file type. "
                "Only .kml and .zip files are allowed."
            )

        if gdf.empty:
            raise ValueError(
                "The uploaded geospatial file contains no features."
            )

        return gdf

    finally:

        shutil.rmtree(
            temporary_directory,
            ignore_errors=True,
        )