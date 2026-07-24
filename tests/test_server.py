"""Unit tests for mcp_caiyun_weather server tools."""

import os

import httpx
import pytest

from mcp_caiyun_weather import __version__, server
from mcp_caiyun_weather.server import (
    REQUEST_TIMEOUT,
    get_historical_weather,
    get_hourly_forecast,
    get_realtime_weather,
    get_weather_alerts,
    get_weekly_forecast,
    make_request,
)


# Test coordinates: Beijing, China
TEST_LNG = 116.3974
TEST_LAT = 39.9093


@pytest.fixture
def stub_async_client(monkeypatch):
    class StubAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_value, traceback):
            return None

    monkeypatch.setattr(server.httpx, "AsyncClient", StubAsyncClient)


@pytest.mark.asyncio
async def test_make_request_sets_user_agent_and_timeout():
    """Test that API requests identify the MCP client and set a timeout."""

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["User-Agent"] == (
            f"mcp-caiyun-weather/{__version__}"
        )
        assert request.extensions["timeout"] == {
            "connect": REQUEST_TIMEOUT,
            "read": REQUEST_TIMEOUT,
            "write": REQUEST_TIMEOUT,
            "pool": REQUEST_TIMEOUT,
        }
        return httpx.Response(200, json={"status": "ok"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        result = await make_request(
            client,
            "https://api.caiyunapp.com/weather",
            {"lang": "en_US"},
        )

    assert result == {"status": "ok"}


@pytest.mark.asyncio
async def test_realtime_weather_includes_sky_condition_and_apparent_temperature(
    monkeypatch,
    stub_async_client,
):
    async def fake_make_request(client, url, params):
        return {
            "result": {
                "realtime": {
                    "temperature": 26,
                    "apparent_temperature": 28.5,
                    "skycon": "PARTLY_CLOUDY_DAY",
                    "humidity": 0.65,
                    "wind": {"speed": 12, "direction": 135},
                    "precipitation": {"local": {"intensity": 0.2}},
                    "air_quality": {
                        "pm25": 12,
                        "pm10": 24,
                        "o3": 80,
                        "so2": 3,
                        "no2": 18,
                        "co": 0.6,
                        "aqi": {"chn": 42, "usa": 38},
                    },
                    "life_index": {
                        "ultraviolet": {"desc": "Moderate"},
                        "comfort": {"desc": "Comfortable"},
                    },
                }
            }
        }

    monkeypatch.setattr(server, "make_request", fake_make_request)

    result = await get_realtime_weather(lng=TEST_LNG, lat=TEST_LAT)

    assert "Apparent Temperature: 28.5°C" in result
    assert "Sky Condition: PARTLY_CLOUDY_DAY" in result


@pytest.mark.asyncio
async def test_hourly_forecast_includes_precipitation_intensity(
    monkeypatch,
    stub_async_client,
):
    requested_params = {}

    async def fake_make_request(client, url, params):
        requested_params.update(params)
        return {
            "result": {
                "hourly": {
                    "temperature": [
                        {"datetime": "2026-07-24T12:00+08:00", "value": 26}
                    ],
                    "skycon": [{"value": "LIGHT_RAIN"}],
                    "precipitation": [{"value": 1.2, "probability": 65}],
                    "wind": [{"speed": 12, "direction": 135}],
                }
            }
        }

    monkeypatch.setattr(server, "make_request", fake_make_request)

    result = await get_hourly_forecast(lng=TEST_LNG, lat=TEST_LAT)

    assert requested_params["hourlysteps"] == "72"
    assert "72-Hour Forecast:" in result
    assert "Precipitation Intensity: 1.2 mm/hr" in result

    result = await get_hourly_forecast(
        lng=TEST_LNG,
        lat=TEST_LAT,
        hours=24,
    )

    assert requested_params["hourlysteps"] == "24"
    assert "24-Hour Forecast:" in result


@pytest.fixture
def api_token():
    """Get API token from environment."""
    token = os.getenv("CAIYUN_WEATHER_API_TOKEN")
    if not token:
        pytest.skip("CAIYUN_WEATHER_API_TOKEN not set")
    return token


class TestGetRealtimeWeather:
    """Tests for get_realtime_weather tool."""

    @pytest.mark.asyncio
    async def test_get_realtime_weather_success(self, api_token):
        """Test successful realtime weather retrieval."""
        result = await get_realtime_weather(lng=TEST_LNG, lat=TEST_LAT)

        # Verify result is a string
        assert isinstance(result, str)
        assert len(result) > 0

        # Verify key information is present
        assert "Temperature:" in result
        assert "Apparent Temperature:" in result
        assert "Sky Condition:" in result
        assert "Humidity:" in result
        assert "Wind:" in result
        assert "Precipitation:" in result
        assert "Air Quality:" in result
        assert "PM2.5:" in result
        assert "PM10:" in result
        assert "AQI:" in result
        assert "Life Index:" in result


class TestGetHourlyForecast:
    """Tests for get_hourly_forecast tool."""

    @pytest.mark.asyncio
    async def test_get_hourly_forecast_success(self, api_token):
        """Test successful hourly forecast retrieval."""
        result = await get_hourly_forecast(lng=TEST_LNG, lat=TEST_LAT)

        # Verify result is a string
        assert isinstance(result, str)
        assert len(result) > 0

        # Verify key information is present
        assert "72-Hour Forecast:" in result
        assert "Time:" in result
        assert "Temperature:" in result
        assert "Weather:" in result
        assert "Rain Probability:" in result
        assert "Precipitation Intensity:" in result
        assert "Wind:" in result


class TestGetWeeklyForecast:
    """Tests for get_weekly_forecast tool."""

    @pytest.mark.asyncio
    async def test_get_weekly_forecast_success(self, api_token):
        """Test successful weekly forecast retrieval."""
        result = await get_weekly_forecast(lng=TEST_LNG, lat=TEST_LAT)

        # Verify result is a string
        assert isinstance(result, str)
        assert len(result) > 0

        # Verify key information is present
        assert "7-Day Forecast:" in result
        assert "Date:" in result
        assert "Temperature:" in result
        assert "Weather:" in result
        assert "Rain Probability:" in result


class TestGetHistoricalWeather:
    """Tests for get_historical_weather tool."""

    @pytest.mark.asyncio
    async def test_get_historical_weather_success(self, api_token):
        """Test successful historical weather retrieval."""
        result = await get_historical_weather(lng=TEST_LNG, lat=TEST_LAT)

        # Verify result is a string
        assert isinstance(result, str)
        assert len(result) > 0

        # Verify key information is present
        assert "Past 24-Hour Weather:" in result
        assert "Time:" in result
        assert "Temperature:" in result
        assert "Weather:" in result


class TestGetWeatherAlerts:
    """Tests for get_weather_alerts tool."""

    @pytest.mark.asyncio
    async def test_get_weather_alerts_success(self, api_token):
        """Test successful weather alerts retrieval."""
        result = await get_weather_alerts(lng=TEST_LNG, lat=TEST_LAT)

        # Verify result is a string
        assert isinstance(result, str)
        assert len(result) > 0

        # Result should either contain alerts or indicate no alerts
        assert (
            "Weather Alerts:" in result or "No active weather alerts." in result
        )
