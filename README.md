# homeassistant integration for brrr.now

## File structure
 ```
 custom_components/brrr/
  ├── __init__.py          — sets up/tears down config entry, loads notify platform via discovery
  ├── manifest.json        — domain: brrr, config_flow: true
  ├── const.py             — DOMAIN, API_BASE_URL, CONF_API_KEY, VALID_SOUNDS, field name constants
  ├── config_flow.py       — UI config flow, stores API key, prevents duplicates
  ├── notify.py            — BrrrNotificationService, builds payload, POSTs to brrr.now API
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

The integration registers `notify.brrr` as a notification action. Call it directly:

```yaml
action: notify.brrr
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

## Creating an Automation with a Time Condition

This guide walks you through creating an automation that fires at a specific time and sends a brrr notification, including optional fields like sound.

### Via the Home Assistant UI

1. Go to **Settings → Automations & Scenes → Automations** and click **+ Create Automation**
2. Click **Create new automation** to open the visual editor

#### Step 1 — Add a Time trigger

1. Under **Triggers**, click **Add Trigger** → select **Time**
2. Set **At** to the time you want, e.g. `07:30:00`

This fires the automation every day at that exact time. For a one-shot trigger on a specific date, use a **Time and Date** (`datetime`) helper instead (see the YAML example below).

#### Step 2 — (Optional) Add a Time condition

Conditions let you restrict the automation to certain days or a time window. To limit it to weekdays only:

1. Under **Conditions**, click **Add Condition** → select **Time**
2. Enable **Weekday** and tick **Mon – Fri**

#### Step 3 — Add the brrr notification action

1. Under **Actions**, click **Add Action** → select **Perform action**
2. In the action search box type `notify.brrr` and select it
3. Switch to **YAML mode** (the `</>` icon in the action card) to set optional fields:

```yaml
action: notify.brrr
data:
  message: "Good morning! Time to start your day."
  title: "Morning Reminder"
  data:
    subtitle: "Have a great day"              # optional — second line of text
    sound: "upbeat_bells"                     # optional — see valid sounds below
    open_url: "https://example.com"           # optional — URL opened on tap
    image_url: "https://example.com/img.png"  # optional — image in notification
    interruption_level: "time-sensitive"      # optional — iOS interruption level
    expiration_date: "2026-12-31T23:59:59"   # optional — discard after this time
    filter_criteria:                          # optional — target specific devices
      device_id: "abc123"
```

4. Click **Save**.

### Full YAML example

Paste this into **Settings → Automations → ⋮ → Edit as YAML** (or into your `automations.yaml`):

```yaml
alias: "Morning brrr notification"
description: "Send a brrr push notification every weekday at 7:30 AM"

trigger:
  - platform: time
    at: "07:30:00"

condition:
  - condition: time
    weekday:
      - mon
      - tue
      - wed
      - thu
      - fri

action:
  - action: notify.brrr
    data:
      message: "Good morning! Time to start your day."
      title: "Morning Reminder"
      data:
        subtitle: "Have a great day"
        sound: "upbeat_bells"
        open_url: "https://example.com"
        image_url: "https://example.com/img.png"
        interruption_level: "time-sensitive"
        # expiration_date: "2026-12-31T23:59:59"  # uncomment to set expiry
        # filter_criteria:                         # uncomment to target a device
        #   device_id: "abc123"

mode: single
```

### Optional field reference

| Field | Type | Description |
|---|---|---|
| `title` | string | Bold heading of the notification |
| `subtitle` | string | Secondary line shown below the title |
| `sound` | string | Sound to play — must be one of the valid values listed below |
| `open_url` | string | URL launched when the user taps the notification |
| `image_url` | string | URL of an image shown inside the notification |
| `interruption_level` | string | iOS interruption level: `passive`, `active`, `time-sensitive`, or `critical` |
| `expiration_date` | string | ISO-8601 datetime after which the notification is discarded |
| `filter_criteria` | dict | Key/value pairs used to target specific devices or groups |

### Valid sounds

```
default           system            brrr              bell_ringing
bubble_ding       bubbly_success_ding  cat_meow        calm1
calm2             cha_ching         dog_barking       door_bell
duck_quack        short_triple_blink   upbeat_bells    warm_soft_error
```

> **Note:** Using an invalid sound value will log an error and abort the notification without sending it.
