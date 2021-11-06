"""
Meter Parser Integration
"""

# import asyncio
# from homeassistant.helpers.config_validation import make_entity_service_schema
# from homeassistant.helpers.entity_component import EntityComponent
# from .const import DOMAIN, PLATFORMS, STARTUP_MESSAGE, SCAN_INTERVAL
# from homeassistant.exceptions import ConfigEntryNotReady
# from homeassistant.core import Config, HomeAssistant
# from homeassistant.config_entries import ConfigEntry
# import logging

# # from custom_components.meterparser.coordinator import MeterParserCoordinator
# SERVICE_SCAN = "scan"
# _LOGGER: logging.Logger = logging.getLogger(__package__)


# async def async_setup(hass: HomeAssistant, config: Config):
#     """Set up the image processing."""
#     component = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)

#     await component.async_setup(config)

#     # async def async_scan_service(service):
#     #     """Service handler for scan."""
#     #     image_entities = await component.async_extract_from_service(service)

#     #     update_tasks = []
#     #     for entity in image_entities:
#     #         entity.async_set_context(service.context)
#     #         update_tasks.append(asyncio.create_task(entity.async_update_ha_state(True)))

#     #     if update_tasks:
#     #         await asyncio.wait(update_tasks)

#     # hass.services.async_register(
#     #     DOMAIN, SERVICE_SCAN, async_scan_service, schema=make_entity_service_schema({})
#     # )

#     return True


# # async def async_setup(hass: HomeAssistant, config: Config):
# #     """Set up the Meter Parser via configuration.yaml."""
# #     if DOMAIN in config:
# #         items = config[DOMAIN]
# #         hass.async_create_task(
# #             hass.config_entries.flow.async_init(
# #                 DOMAIN, context={"source": "import"}, data=items
# #             )
# #         )
# #     return True


# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
#     """Set up this integration using UI."""
#     if hass.data.get(DOMAIN) is None:
#         hass.data.setdefault(DOMAIN, {})
#         _LOGGER.info(STARTUP_MESSAGE)

#     for component in PLATFORMS:
#         hass.async_create_task(
#             hass.config_entries.async_forward_entry_setup(entry, component)
#         )

#     entry.add_update_listener(async_reload_entry)
#     return True


# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Handle removal of an entry."""
#     for component in PLATFORMS:
#         await hass.config_entries.async_forward_entry_unload(entry, component)

#     return True


# async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
#     """Reload config entry."""
#     await async_unload_entry(hass, entry)
#     await async_setup_entry(hass, entry)
