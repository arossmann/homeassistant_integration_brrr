# homeassistant integration for brrr.now

## File structure
 ```
 custom_components/brrr/
  ├── __init__.py          — sets up/tears down config entry, forwards to notify platform
  ├── manifest.json        — domain: brrr, config_flow: true
  ├── const.py             — DOMAIN, API_BASE_URL, CONF_API_KEY, VALID_SOUNDS, field name constants
  ├── config_flow.py       — UI config flow, stores API key + optional defaults, prevents duplicates
  ├── notify.py            — BrrrNotifyEntity, builds payload from config + message, POSTs to brrr.now API
  ├── strings.json         — UI text (config flow)
  └── translations/
      └── en.json          — English translations
```

## Installation
see [installaton](./docs/installation.md)

## Usage
see [usage](./docs/usage.md)
