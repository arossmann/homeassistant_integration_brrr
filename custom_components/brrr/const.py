"""Constants for the brrr integration."""

DOMAIN = "brrr"

CONF_API_KEY = "api_key"

API_BASE_URL = "https://api.brrr.now/v1/"

VALID_SOUNDS = [
    "default",
    "system",
    "brrr",
    "bell_ringing",
    "bubble_ding",
    "bubbly_success_ding",
    "cat_meow",
    "calm1",
    "calm2",
    "cha_ching",
    "dog_barking",
    "door_bell",
    "duck_quack",
    "short_triple_blink",
    "upbeat_bells",
    "warm_soft_error",
]

ATTR_SUBTITLE = "subtitle"
ATTR_SOUND = "sound"
ATTR_OPEN_URL = "open_url"
ATTR_IMAGE_URL = "image_url"
ATTR_EXPIRATION_DATE = "expiration_date"
ATTR_FILTER_CRITERIA = "filter_criteria"
ATTR_INTERRUPTION_LEVEL = "interruption_level"

VALID_INTERRUPTION_LEVELS = [
    "passive",
    "active",
    "time-sensitive",
    "critical",
]
