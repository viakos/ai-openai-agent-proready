"""
Async, retriable call to Open‑Meteo public API.
"""

from typing import Dict
import httpx
import backoff


@backoff.on_exception(backoff.expo, httpx.HTTPError, max_tries=3, jitter=None)
async def fetch_weather(latitude: float, longitude: float) -> Dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,relative_humidity_2m,dew_point_2m,"
            "apparent_temperature,precipitation,weathercode,"
            "windspeed_10m,winddirection_10m"
        ),
        "timezone": "auto",
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()
