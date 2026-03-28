# homeassistant integration for brrr.now

## File structure
 ```
 custom_components/brrr/
  ├── __init__.py          — sets up/tears down config entry, forwards to notify platform
  ├── manifest.json        — domain: brrr, config_flow: true
  ├── const.py             — DOMAIN, API_BASE_URL, CONF_API_KEY, VALID_SOUNDS, field name constants
  ├── config_flow.py       — UI config flow, stores API key, prevents duplicates
  ├── notify.py            — BrrrNotifyEntity, builds payload, POSTs to brrr.now API
  ├── strings.json         — UI text (config flow)
  └── translations/
      └── en.json          — English translations
```

## Installation

### Via HACS (recommended)

1. In HACS, go to **Integrations** → click the three-dot menu → **Custom repositories**
2. Add this repository URL and select category **Integration**
3. Click **Download** on the brrr integration
4. Restart Home Assistant
5. Go to **Settings → Integrations → Add Integration** and search for **brrr**

### Manual

Copy the `custom_components/brrr/` folder into your HA `config/custom_components/` directory, restart HA, then go to **Settings → Integrations → Add Integration → search "brrr"**.

## Usage

To use in an automation:
```yaml
service: notify.brrr
data:
  message: "Hello from HA"
  title: "My Title"
  data:
    subtitle: "Optional subtitle"
    sound: "cha_ching"
    open_url: "https://example.com"
    image_url: "https://example.com/image.png"
    interruption_level: "time-sensitive"
```
