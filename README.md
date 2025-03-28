# Caiyun Weather MCP Server

## Setup Instructions

> Before anything, ensure you have access to the API. You can apply for it at [https://docs.caiyunapp.com/weather-api/](https://docs.caiyunapp.com/weather-api/).

Install uv first.

MacOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup with Claude Desktop

```
# claude_desktop_config.json
# Can find location through:
# Hamburger Menu -> File -> Settings -> Developer -> Edit Config
{
  "mcpServers": {
    "caiyun-weather": {
      "command": "uvx",
      "args": ["mcp-caiyun-weather"],
      "env": {
        "CAIYUN_WEATHER_API_TOKEN": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

### Ask Claude a question requiring weather
e.g. "What's the weather in Beijing Now?"

## Local/Dev Setup Instructions

### Setup with Claude Desktop

```
# claude_desktop_config.json
# Can find location through:
# Hamburger Menu -> File -> Settings -> Developer -> Edit Config
{
  "mcpServers": {
    "caiyun-weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp-caiyun-weather",
        "run",
        "mcp-caiyun-weather"
      ],
      "env": {
        "CAIYUN_WEATHER_API_TOKEN": "YOUR_API_TOKEN_HERE"
      }
    }
  }
}
```

### Debugging

Run:
```bash
npx @modelcontextprotocol/inspector \
      uv \
      --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp-caiyun-weather \
      run \
      mcp-caiyun-weather
```

## Available Tools

- `get_realtime_weather`: Get real-time weather data for a specific location
  - Parameters:
    - `lng`: The longitude of the location
    - `lat`: The latitude of the location
  - Returns detailed information including:
    - Temperature
    - Humidity
    - Wind speed and direction
    - Precipitation intensity
    - Air quality metrics (PM2.5, PM10, O3, SO2, NO2, CO)
    - AQI (China and USA standards)
    - Life indices (UV and Comfort)

- `get_hourly_forecast`: Get hourly weather forecast for the next 72 hours
  - Parameters:
    - `lng`: The longitude of the location
    - `lat`: The latitude of the location
  - Returns hourly forecast including:
    - Temperature
    - Weather conditions
    - Rain probability
    - Wind speed and direction

- `get_weekly_forecast`: Get daily weather forecast for the next 7 days
  - Parameters:
    - `lng`: The longitude of the location
    - `lat`: The latitude of the location
  - Returns daily forecast including:
    - Temperature range (min/max)
    - Weather conditions
    - Rain probability

- `get_historical_weather`: Get historical weather data for the past 24 hours
  - Parameters:
    - `lng`: The longitude of the location
    - `lat`: The latitude of the location
  - Returns historical data including:
    - Temperature
    - Weather conditions

- `get_weather_alerts`: Get weather alerts for a specific location
  - Parameters:
    - `lng`: The longitude of the location
    - `lat`: The latitude of the location
  - Returns weather alerts including:
    - Alert title
    - Alert code
    - Alert status
    - Alert description

Note: All tools require a valid Caiyun Weather API token to be set in the environment variable `CAIYUN_WEATHER_API_TOKEN`.
