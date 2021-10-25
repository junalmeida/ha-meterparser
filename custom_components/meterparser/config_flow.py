"""Adds config flow for Meter Parser."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import (
    CONF_URI,
    CONF_METERTYPE,
    CONF_ENERGY,
    DOMAIN,
    ENERGYTYPES,
    METERTYPES,
    PLATFORMS,
)


class MeterParserFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for MeterParser."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        user_input = {}
        # Provide defaults for form
        user_input[CONF_URI] = ""
        user_input[CONF_ENERGY] = ""
        user_input[CONF_METERTYPE] = ""

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MeterParserOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URI, default=user_input[CONF_URI]): str,
                    vol.Required(CONF_METERTYPE, default=user_input[CONF_METERTYPE]): vol.In(METERTYPES),
                    vol.Required(CONF_ENERGY, default=user_input[CONF_ENERGY]): vol.In(ENERGYTYPES)
                }
            ),
            errors=self._errors,
        )


class MeterParserOptionsFlowHandler(config_entries.OptionsFlow):
    """MeterParser config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_URI), data=self.options
        )
