import os
from datetime import datetime, timedelta

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


@mcp.tool()
async def get_hourly_forecast(
    lng: float = Field(
        description="The longitude of the location to get the weather for"
    ),
    lat: float = Field(
        description="The latitude of the location to get the weather for"
    ),
) -> dict:
    """Get hourly weather forecast for the next 72 hours."""
    try:
        async with httpx.AsyncClient() as client:
            result = await make_request(
                client,
                f"https://api.caiyunapp.com/v2.6/{api_token}/{lng},{lat}/hourly",
                {"hourlysteps": "72", "lang": "en_US"},
            )
            hourly = result["result"]["hourly"]
            forecast = "72-Hour Forecast:\n"
            for i in range(len(hourly["temperature"])):
                time = hourly["temperature"][i]["datetime"].split("+")[0]
                temp = hourly["temperature"][i]["value"]
                skycon = hourly["skycon"][i]["value"]
                rain_prob = hourly["precipitation"][i]["probability"]
                wind_speed = hourly["wind"]["speed"][i]["value"]
                wind_dir = hourly["wind"]["direction"][i]["value"]

                forecast += f"""
Time: {time}
Temperature: {temp}°C
Weather: {skycon}
Rain Probability: {rain_prob}%
Wind: {wind_speed}m/s, {wind_dir}°
------------------------"""
            return forecast
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


@mcp.tool()
async def get_weekly_forecast(
    lng: float = Field(
        description="The longitude of the location to get the weather for"
    ),
    lat: float = Field(
        description="The latitude of the location to get the weather for"
    ),
) -> dict:
    """Get daily weather forecast for the next 7 days."""
    try:
        async with httpx.AsyncClient() as client:
            result = await make_request(
                client,
                f"https://api.caiyunapp.com/v2.6/{api_token}/{lng},{lat}/daily",
                {"dailysteps": "7", "lang": "en_US"},
            )
            daily = result["result"]["daily"]
            forecast = "7-Day Forecast:\n"
            for i in range(7):
                date = daily["temperature"][i]["date"].split("T")[0]
                temp_max = daily["temperature"][i]["max"]
                temp_min = daily["temperature"][i]["min"]
                skycon = daily["skycon"][i]["value"]
                rain_prob = daily["precipitation"][i]["probability"]

                forecast += f"""
Date: {date}
Temperature: {temp_min}°C ~ {temp_max}°C
Weather: {skycon}
Rain Probability: {rain_prob}%
------------------------"""
            return forecast
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


@mcp.tool()
async def get_historical_weather(
    lng: float = Field(
        description="The longitude of the location to get the weather for"
    ),
    lat: float = Field(
        description="The latitude of the location to get the weather for"
    ),
) -> dict:
    """Get historical weather data for the past 24 hours."""
    try:
        # Calculate timestamp for 24 hours ago
        timestamp = int((datetime.now() - timedelta(hours=24)).timestamp())

        async with httpx.AsyncClient() as client:
            result = await make_request(
                client,
                f"https://api.caiyunapp.com/v2.6/{api_token}/{lng},{lat}/hourly",
                {"hourlysteps": "24", "begin": str(timestamp), "lang": "en_US"},
            )
            hourly = result["result"]["hourly"]
            history = "Past 24-Hour Weather:\n"
            for i in range(len(hourly["temperature"])):
                time = hourly["temperature"][i]["datetime"].split("+")[0]
                temp = hourly["temperature"][i]["value"]
                skycon = hourly["skycon"][i]["value"]

                history += f"""
Time: {time}
Temperature: {temp}°C
Weather: {skycon}
------------------------"""
            return history
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


@mcp.tool()
async def get_weather_alerts(
    lng: float = Field(
        description="The longitude of the location to get the weather for"
    ),
    lat: float = Field(
        description="The latitude of the location to get the weather for"
    ),
) -> dict:
    """Get weather alerts for the location."""
    try:
        async with httpx.AsyncClient() as client:
            result = await make_request(
                client,
                f"https://api.caiyunapp.com/v2.6/{api_token}/{lng},{lat}/weather",
                {"alert": "true", "lang": "en_US"},
            )
            alerts = result["result"].get("alert", {}).get("content", [])
            if not alerts:
                return "No active weather alerts."

            alert_text = "Weather Alerts:\n"
            for alert in alerts:
                alert_text += f"""
Title: {alert.get("title", "N/A")}
Code: {alert.get("code", "N/A")}
Status: {alert.get("status", "N/A")}
Description: {alert.get("description", "N/A")}
------------------------"""
            return alert_text
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def main():
    mcp.run()
