"""
Meter Parser Integration
"""

from .const import (
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.core import Config, HomeAssistant
from homeassistant.config_entries import ConfigEntry
import logging

# from custom_components.meterparser.coordinator import MeterParserCoordinator

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up the Meter Parser via configuration.yaml."""
    if DOMAIN in config:
        items = config[DOMAIN]
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": "import"}, data=items
            )
        )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    # coordinator = MeterParserCoordinator(hass, entry)
    # await coordinator.async_refresh()

    # if not coordinator.last_update_success:
    # raise ConfigEntryNotReady

    # hass.data[DOMAIN][entry.entry_id] = coordinator

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    for component in PLATFORMS:
        await hass.config_entries.async_forward_entry_unload(entry, component)

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
