"""Adds config flow for Meter Parser."""
from homeassistant import config_entries
import voluptuous as vol

from .const import (
    CONF_URI,
    CONF_METERTYPE,
    CONF_UTILITYTYPE,
    CONF_ZOOMFACTOR,
    CONF_DEBUG,
    DOMAIN,
    CONF_COUNT,
    CONF_AVGSIZE,
    UTILITYTYPES,
    METERTYPES
)


class MeterParserFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Meter Parser config flow."""

    def __init__(self):
        """Initialize."""
        self.uri = None
        self.zoomfactor = 1.0
        self.metertype = METERTYPES[0]
        self.utilitytype = UTILITYTYPES[0]
        self.avgsize = 100
        self.dials = 4
        self.debug = False

    def _get_entry(self):
        return self.async_create_entry(
            title="%s Meter" % self.utilitytype,
            data={
                CONF_URI: self.uri,
                CONF_ZOOMFACTOR: self.zoomfactor,
                CONF_METERTYPE: self.metertype,
                CONF_UTILITYTYPE: self.utilitytype,
                CONF_AVGSIZE: self.avgsize,
                CONF_COUNT: self.dials,
                CONF_DEBUG: self.debug
            },
        )

    async def async_step_import(self, user_input=None):
        """Handle configuration by yaml file."""
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        """Handle configuration via user input."""
        errors = {}
        if user_input is not None:
            self.uri = user_input[CONF_URI]
            self.zoomfactor = user_input[CONF_ZOOMFACTOR]
            self.metertype = user_input[CONF_METERTYPE]
            self.utilitytype = user_input[CONF_UTILITYTYPE]
            self.avgsize = user_input[CONF_AVGSIZE]
            self.dials = user_input[CONF_COUNT]
            self.debug = user_input[CONF_DEBUG]

            await self.async_set_unique_id(self.uri)
            self._abort_if_unique_id_configured()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_URI, default=self.uri): vol.Strip(),
                vol.Required(CONF_UTILITYTYPE, default=self.utilitytype): vol.In(UTILITYTYPES),
                vol.Required(CONF_METERTYPE, default=self.metertype): vol.In(METERTYPES),
                vol.Optional(CONF_AVGSIZE, default=self.avgsize): vol.Number(precision=3, scale=0),
                vol.Optional(CONF_ZOOMFACTOR, default=self.zoomfactor): vol.Number(precision=1, scale=2),
                vol.Optional(CONF_DEBUG, default=self.debug): vol.Boolean()
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_unignore(self, user_input):
        """Rediscover a previously ignored discover."""
        unique_id = user_input["unique_id"]
        await self.async_set_unique_id(unique_id)
        return await self.async_step_user()
