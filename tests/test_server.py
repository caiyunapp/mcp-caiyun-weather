"""Unit tests for mcp_caiyun_weather server tools."""

import os

import pytest

from mcp_caiyun_weather.server import (
    get_historical_weather,
    get_hourly_forecast,
    get_realtime_weather,
    get_weather_alerts,
    get_weekly_forecast,
)


# Test coordinates: Beijing, China
TEST_LNG = 116.3974
TEST_LAT = 39.9093


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
