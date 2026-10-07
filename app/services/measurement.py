from typing import Any

from shapely.geometry import mapping

from app.services.crs import prepare_for_measurement


SUPPORTED_AREA_TYPES = {
    "Polygon",
    "MultiPolygon",
}

SUPPORTED_LENGTH_TYPES = {
    "LineString",
    "MultiLineString",
}


def make_json_safe(value: Any):
    """
    Convert values that are not JSON serializable into strings.
    """

    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    return str(value)


def serialize_properties(properties):
    return {
        str(key): make_json_safe(value)
        for key, value in properties.items()
    }


def calculate_measurements(gdf):

    source_crs = (
        gdf.crs.to_string()
        if gdf.crs is not None
        else None
    )

    measurement_gdf, measurement_crs = prepare_for_measurement(gdf)

    features = []

    for index, row in measurement_gdf.iterrows():

        geometry = row.geometry

        if geometry is None or geometry.is_empty:
            features.append(
                {
                    "feature_id": int(index),
                    "geometry_type": "Unknown",
                    "geometry": {},
                    "properties": serialize_properties(
                        row.drop(labels=["geometry"]).to_dict()
                    ),
                    "area_m2": None,
                    "length_m": None,
                }
            )
            continue

        geometry_type = geometry.geom_type

        area_m2 = None
        length_m = None

        if geometry_type in SUPPORTED_AREA_TYPES:
            area_m2 = float(geometry.area)

        elif geometry_type in SUPPORTED_LENGTH_TYPES:
            length_m = float(geometry.length)

        elif geometry_type == "Point":
            pass

        else:
            pass

        properties = {
            column: row[column]
            for column in measurement_gdf.columns
            if column != "geometry"
        }

        features.append(
            {
                "feature_id": int(index),
                "geometry_type": geometry_type,
                "geometry": mapping(geometry),
                "properties": serialize_properties(properties),
                "area_m2": area_m2,
                "length_m": length_m,
            }
        )

    return {
        "source_crs": source_crs,
        "measurement_crs": measurement_crs.to_string(),
        "features": features,
    }