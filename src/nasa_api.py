import requests


def fetch_rainfall_data(lat, lon, start="20250501", end="20250830"):
    """Fetch PRECTOTCORR (corrected precipitation) from NASA POWER for a point.
    Returns the sum of daily precipitation (mm) for the requested window or None on failure.
    """
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "PRECTOTCORR",
        "community": "AG",
        "longitude": float(lon),
        "latitude": float(lat),
        "start": str(start),
        "end": str(end),
        "format": "JSON",
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        rain_values = data.get("properties", {}).get("parameter", {}).get("PRECTOTCORR", {})
        if not rain_values:
            return None
        return sum(float(v) for v in rain_values.values())
    except Exception:
        return None
