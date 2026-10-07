# Geospatial File Measurement API

A FastAPI-based geospatial processing API that accepts KML files and
Shapefile ZIP archives, extracts geographic features, handles CRS
transformations, and calculates area and length measurements.

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
