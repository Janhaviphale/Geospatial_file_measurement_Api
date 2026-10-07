from shapely.geometry import LineString, Point, Polygon

from app.services.measurement import (
    SUPPORTED_AREA_TYPES,
    SUPPORTED_LENGTH_TYPES,
)


def test_polygon_is_supported():
    assert "Polygon" in SUPPORTED_AREA_TYPES


def test_multipolygon_is_supported():
    assert "MultiPolygon" in SUPPORTED_AREA_TYPES


def test_linestring_is_supported():
    assert "LineString" in SUPPORTED_LENGTH_TYPES


def test_point_requires_no_measurement():
    point = Point(10, 20)
    assert point.geom_type == "Point"


def test_polygon_area():
    polygon = Polygon(
        [
            (0, 0),
            (10, 0),
            (10, 10),
            (0, 10),
        ]
    )

    assert polygon.area == 100


def test_linestring_length():
    line = LineString(
        [
            (0, 0),
            (3, 4),
        ]
    )

    assert line.length == 5