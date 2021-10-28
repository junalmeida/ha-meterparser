from datetime import timedelta
from config.custom_components.meterparser.coordinator import MeterParserCoordinator
from homeassistant import config_entries, core
from .const import (
    CONF_METERTYPE,
    CONF_UTILITYTYPE,
    DEFAULT_NAME,
    DOMAIN,
    SENSOR,
    UTILITYGAS,
    UTILITYWATER,
)
from .entity import MeterParserEntity
from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    ENERGY_KILO_WATT_HOUR,
    VOLUME_CUBIC_METERS,
)

# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(minutes=10)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensor platform."""
    # coordinator: MeterParserCoordinator = hass.data[DOMAIN][entry.entry_id]
    for item in coordinator.config_entry.data:
        async_add_devices([MeterParserSensor(coordinator, item)])


class MeterParserSensor(MeterParserEntity):
    def __init__(self, coordinator, entry):
        """Initialize"""
        self.coordinator = coordinator
        self.metertype = entry[CONF_METERTYPE]
        self.utilitytype = entry[CONF_UTILITYTYPE]

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data

    @property
    def device_class(self):
        return DEVICE_CLASS_ENERGY

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self.utilitytype == UTILITYGAS:
            return "mdi:fire"
        elif self.utilitytype == UTILITYWATER:
            return "mdi:water"
        else:
            return "mdi:lightning"
