# Geospatial File Measurement API

A FastAPI-based geospatial processing API that accepts KML files and
Shapefile ZIP archives, extracts geographic features, handles CRS
transformations, and calculates area and length measurements.

---

## 📸 Screenshots

### 1. Swagger API Documentation

![Swagger API Documentation](<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/4fdd0bd7-2510-4afe-9d50-f8fa1b5f21cc" />
)

The API provides interactive Swagger documentation for testing all
available endpoints.

### 2. File Upload

![File Upload](screenshots/upload.png)

KML and Shapefile ZIP files can be uploaded through the API.

### 3. File Information

![File Information](screenshots/file-info.png)

The API returns the uploaded file ID, filename, feature count,
source CRS, measurement CRS, and processing status.

### 4. Measurements

![Measurements](screenshots/measurements.png)

The measurements endpoint returns geometry information, properties,
area in square meters, and length in meters.

### 5. Test Results

![Test Results](screenshots/tests.png)

All automated tests pass successfully.

---

## 🚀 Features

- Upload `.kml` files
- Upload `.zip` files containing Shapefiles
- Extract geospatial features
- Identify geometry types
- Return feature properties
- Calculate polygon area
- Calculate LineString length
- Handle Point geometries
- Automatically transform geographic CRS to a suitable projected CRS
- Store file metadata and measurements in SQLite
- Interactive Swagger API documentation
- Input validation and error handling
- ZIP path traversal protection
- Automated tests
- Docker support

---

## 🛠️ Tech Stack

- Python
- FastAPI
- GeoPandas
- Shapely
- PyProj
- Fiona
- SQLAlchemy
- SQLite
- Pytest
- Docker

---

## 📁 Project Structure

```text
geospatial-file-measurement-api/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   └── file_record.py
│   ├── schemas/
│   │   └── file_schema.py
│   ├── services/
│   │   ├── crs.py
│   │   ├── file_processor.py
│   │   └── measurement.py
│   └── main.py
│
├── tests/
│   ├── test_api.py
│   └── test_measurement.py
│
├── storage/
├── Dockerfile
├── README.md
├── requirements.txt
└── run.py
