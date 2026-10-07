from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

STORAGE_DIR = BASE_DIR / "storage"

DATABASE_URL = f"sqlite:///{BASE_DIR / 'geospatial.db'}"

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

ALLOWED_EXTENSIONS = {".kml", ".zip"}