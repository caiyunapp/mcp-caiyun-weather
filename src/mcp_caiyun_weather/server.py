import os

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import Field


mcp = FastMCP("caiyun-weather", dependencies=["mcp[cli]"])

api_token = os.getenv("CAIYUN_WEATHER_API_TOKEN")


async def make_request(client: httpx.AsyncClient, url: str, params: dict) -> dict:
    response = await client.get(url, params=params)
    response.raise_for_status()
    return response.json()


@mcp.tool()
async def get_realtime_weather(
    lng: float = Field(
        description="The longitude of the location to get the weather for"
    ),
    lat: float = Field(
        description="The latitude of the location to get the weather for"
    ),
) -> dict:
    """Get the realtime weather for a location."""
    try:
        async with httpx.AsyncClient() as client:
            result = await make_request(
                client,
                f"https://api.caiyunapp.com/v2.6/{api_token}/{lng},{lat}/realtime",
                {"lang": "en_US"},
            )
            result = result["result"]["realtime"]
            return f"""
Temperature: {result["temperature"]}°C
Humidity: {result["humidity"]}%
Wind: {result["wind"]["speed"]} m/s, From north clockwise {result["wind"]["direction"]}°
Precipitation: {result["precipitation"]["local"]["intensity"]}%
Air Quality:
    PM2.5: {result["air_quality"]["pm25"]} μg/m³
    PM10: {result["air_quality"]["pm10"]} μg/m³
    O3: {result["air_quality"]["o3"]} μg/m³
    SO2: {result["air_quality"]["so2"]} μg/m³
    NO2: {result["air_quality"]["no2"]} μg/m³
    CO: {result["air_quality"]["co"]} mg/m³
    AQI:
        China: {result["air_quality"]["aqi"]["chn"]}
        USA: {result["air_quality"]["aqi"]["usa"]}
    Life Index:
        UV: {result["life_index"]["ultraviolet"]["desc"]}
        Comfort: {result["life_index"]["comfort"]["desc"]}
"""
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def main():
    mcp.run()
