"""Adds config flow for Meter Parser."""
from typing import Any, Dict
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
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
    NAME,
    UTILITYTYPES,
    METERTYPES,
)

ADD_MORE = "add_more"


class MeterParserConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Meter Parser config flow."""

    def __init__(self):
        """Initialize."""
        default_meter = next(iter(METERTYPES))
        default_utility = next(iter(UTILITYTYPES))

        self.data = [
            {
                CONF_URI: None,
                CONF_ZOOMFACTOR: 1.0,
                CONF_METERTYPE: default_meter,
                CONF_UTILITYTYPE: default_utility,
                CONF_AVGSIZE: 100,
                CONF_COUNT: 4,
                CONF_DEBUG: False,
            }
        ]

    def _get_entry(self):
        return self.async_create_entry(
            title="%s Meter" % self.data[CONF_UTILITYTYPE],
            data=self.data,
        )

    async def async_step_import(self, user_input=None):
        """Handle configuration by yaml file."""
        self.data = user_input

        return self.async_create_entry(title=NAME, data=self.data)

    async def async_step_user(self, user_input=None):
        """Handle configuration via user input."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if self.hass.data.get(DOMAIN):
            return self.async_abort(reason="single_instance_allowed")
        errors = {}

        if user_input is not None:
            self.data.append(user_input)

        if user_input is not None and user_input[ADD_MORE] is False:
            # await self.async_set_unique_id(self.data[CONF_UTILITYTYPE])
            # self._abort_if_unique_id_configured()
            return self.async_create_entry(title=NAME, data=self.data)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_URI, default=self.data[CONF_URI]): cv.string,
                vol.Required(
                    CONF_UTILITYTYPE, default=self.data[CONF_UTILITYTYPE]
                ): vol.In(UTILITYTYPES),
                vol.Required(CONF_METERTYPE, default=self.data[CONF_METERTYPE]): vol.In(
                    METERTYPES
                ),
                vol.Optional(
                    CONF_AVGSIZE, default=self.data[CONF_AVGSIZE]
                ): cv.positive_int,
                vol.Optional(
                    CONF_ZOOMFACTOR, default=self.data[CONF_ZOOMFACTOR]
                ): cv.positive_float,
                vol.Optional(CONF_DEBUG, default=self.data[CONF_DEBUG]): cv.boolean,
                vol.Optional(ADD_MORE, default=False): cv.boolean,
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


#     @staticmethod
#     @callback
#     def async_get_options_flow(config_entry):
#         """Get the options flow for this handler."""
#         return MeterParserOptionsFlow(config_entry)


# class MeterParserOptionsFlow(config_entries.OptionsFlow):
#     """Handles options flow for the component."""

#     def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
#         self.config_entry = config_entry

#     async def async_step_init(
#         self, user_input: Dict[str, Any] = None
#     ) -> Dict[str, Any]:
#         """Manage the options for the custom component."""
#         errors: Dict[str, str] = {}

#         if user_input is not None:
#             self.config_entry.data = user_input

#             if not errors:
#                 # Value of data will be set on the options property of our config_entry
#                 # instance.
#                 return self.async_create_entry(
#                     title=self.config_entry.data[CONF_UTILITYTYPE],
#                     data=self.config_entry.data,
#                 )

#         options_schema = vol.Schema(
#             {
#                 vol.Required(
#                     CONF_URI, default=self.config_entry.data[CONF_URI]
#                 ): cv.string,
#                 vol.Required(
#                     CONF_METERTYPE, default=self.config_entry.data[CONF_METERTYPE]
#                 ): vol.In(METERTYPES),
#                 vol.Optional(
#                     CONF_AVGSIZE, default=self.config_entry.data[CONF_AVGSIZE]
#                 ): cv.positive_int,
#                 vol.Optional(
#                     CONF_ZOOMFACTOR, default=self.config_entry.data[CONF_ZOOMFACTOR]
#                 ): cv.positive_float,
#                 vol.Optional(
#                     CONF_DEBUG, default=self.config_entry.data[CONF_DEBUG]
#                 ): cv.boolean,
#             }
#         )
#         return self.async_show_form(
#             step_id="user", data_schema=options_schema, errors=errors
#         )
