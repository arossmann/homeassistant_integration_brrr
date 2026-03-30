"""brrr notification platform."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.notify import (
    ATTR_TITLE,
    NotifyEntity,
    NotifyEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    API_BASE_URL,
    ATTR_EXPIRATION_DATE,
    ATTR_FILTER_CRITERIA,
    ATTR_IMAGE_URL,
    ATTR_INTERRUPTION_LEVEL,
    ATTR_OPEN_URL,
    ATTR_SOUND,
    ATTR_SUBTITLE,
    CONF_API_KEY,
    VALID_SOUNDS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the brrr notify entity from a config entry."""
    api_key = config_entry.data[CONF_API_KEY]
    session = async_get_clientsession(hass)
    async_add_entities([BrrrNotifyEntity(api_key, session, dict(config_entry.data))])


class BrrrNotifyEntity(NotifyEntity):
    """Representation of a brrr notification service."""

    _attr_name = "brrr"
    _attr_supported_features = NotifyEntityFeature.TITLE

    def __init__(self, api_key: str, session: Any, config: dict) -> None:
        self._api_key = api_key
        self._session = session
        self._config = config
        self._attr_unique_id = f"brrr_{api_key}"

    async def async_send_message(self, message: str, **kwargs: Any) -> None:
        """Send a notification via brrr.now."""
        title = kwargs.get(ATTR_TITLE)

        payload: dict[str, Any] = {"message": message}

        if title:
            payload["title"] = title

        if subtitle := self._config.get(ATTR_SUBTITLE):
            payload["subtitle"] = subtitle

        if sound := self._config.get(ATTR_SOUND):
            if sound not in VALID_SOUNDS:
                _LOGGER.error(
                    "Invalid sound '%s'. Valid values: %s",
                    sound,
                    ", ".join(VALID_SOUNDS),
                )
                return
            payload["sound"] = sound

        if open_url := self._config.get(ATTR_OPEN_URL):
            payload["open_url"] = open_url

        if image_url := self._config.get(ATTR_IMAGE_URL):
            payload["image_url"] = image_url

        if expiration_date := self._config.get(ATTR_EXPIRATION_DATE):
            payload["expiration_date"] = expiration_date

        # Translate underscore field names to the hyphenated keys the API expects
        if filter_criteria := self._config.get(ATTR_FILTER_CRITERIA):
            payload["filter-criteria"] = filter_criteria

        if interruption_level := self._config.get(ATTR_INTERRUPTION_LEVEL):
            payload["interruption-level"] = interruption_level

        url = f"{API_BASE_URL}{self._api_key}"
        try:
            response = await self._session.post(url, json=payload)
            response.raise_for_status()
        except Exception as err:  # noqa: BLE001
            _LOGGER.error("Failed to send brrr notification: %s", err)
