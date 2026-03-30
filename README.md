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

### Via HACS (recommended)

1. In HACS, go to **Integrations** → click the three-dot menu → **Custom repositories**
2. Add this repository URL and select category **Integration**
3. Click **Download** on the brrr integration
4. Restart Home Assistant
5. Go to **Settings → Integrations → Add Integration** and search for **brrr**

### Manual

Copy the `custom_components/brrr/` folder into your HA `config/custom_components/` directory, restart HA, then go to **Settings → Integrations → Add Integration → search "brrr"**.

## Usage

Optional fields (sound, interruption level, subtitle, open URL, image URL) are configured once when you add the integration — no need to set them per automation.

In an automation, just provide the message and an optional title:

```yaml
action: notify.send_message
target:
  entity_id: notify.brrr
data:
  message: "Hello from HA"
  title: "My Title"
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
2. In the action search box type `notify.send_message` and select it
3. In the **Target** field, pick the entity **brrr**
4. Fill in **Message** and optionally **Title**

```yaml
action: notify.send_message
target:
  entity_id: notify.brrr
data:
  message: "Good morning! Time to start your day."
  title: "Morning Reminder"
```

Sound, interruption level, and other defaults will be applied automatically from the integration configuration.

5. Click **Save**.

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
  - action: notify.send_message
    target:
      entity_id: notify.brrr
    data:
      message: "Good morning! Time to start your day."
      title: "Morning Reminder"

mode: single
```

### Configuration options

Set these when adding the integration (**Settings → Devices & Services → Add Integration → brrr**). They apply to every notification sent by this integration instance.

| Field | Description |
|---|---|
| **API Key** *(required)* | Your brrr.now API key |
| **Default Sound** | Sound played with every notification — see valid values below |
| **Interruption Level** | iOS interruption level: `passive`, `active`, `time-sensitive`, `critical` |
| **Default Subtitle** | Secondary line shown below the title |
| **Default Open URL** | URL opened when the notification is tapped |
| **Default Image URL** | Image shown inside the notification |

### Valid sounds

```
default           system            brrr              bell_ringing
bubble_ding       bubbly_success_ding  cat_meow        calm1
calm2             cha_ching         dog_barking       door_bell
duck_quack        short_triple_blink   upbeat_bells    warm_soft_error
```

> **Note:** Using an invalid sound value will log an error and abort the notification without sending it.
