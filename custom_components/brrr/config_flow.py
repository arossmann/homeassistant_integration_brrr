"""Config flow for the brrr integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    ATTR_IMAGE_URL,
    ATTR_INTERRUPTION_LEVEL,
    ATTR_OPEN_URL,
    ATTR_SOUND,
    ATTR_SUBTITLE,
    CONF_API_KEY,
    DOMAIN,
    VALID_INTERRUPTION_LEVELS,
    VALID_SOUNDS,
)


class BrrrConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for brrr."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_API_KEY])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="brrr", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Optional(ATTR_SOUND): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=VALID_SOUNDS,
                            mode=selector.SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Optional(ATTR_INTERRUPTION_LEVEL): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=VALID_INTERRUPTION_LEVELS,
                            mode=selector.SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Optional(ATTR_SUBTITLE): selector.TextSelector(),
                    vol.Optional(ATTR_OPEN_URL): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.URL
                        )
                    ),
                    vol.Optional(ATTR_IMAGE_URL): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.URL
                        )
                    ),
                }
            ),
        )
