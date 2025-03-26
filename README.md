# mcp-caiyun-weather

## Setup Instructions

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
