import geopandas as gpd


def get_measurement_crs(gdf: gpd.GeoDataFrame):
    """
    Return a projected CRS suitable for measurement.

    If the input CRS is already projected, use it directly.

    If the input CRS is geographic, automatically estimate
    an appropriate UTM CRS based on the geometry location.
    """

    if gdf.crs is None:
        raise ValueError(
            "Input file does not contain a CRS. "
            "A valid CRS is required for measurement."
        )

    if gdf.crs.is_projected:
        return gdf.crs

    estimated_crs = gdf.estimate_utm_crs()

    if estimated_crs is None:
        raise ValueError(
            "Could not determine a suitable projected CRS "
            "for the uploaded geometry."
        )

    return estimated_crs


def prepare_for_measurement(gdf: gpd.GeoDataFrame):
    """
    Transform the GeoDataFrame into a projected CRS suitable
    for area and length calculations.
    """

    measurement_crs = get_measurement_crs(gdf)

    if gdf.crs != measurement_crs:
        gdf = gdf.to_crs(measurement_crs)

    return gdf, measurement_crs