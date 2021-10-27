from .const import CONF_METERTYPE, CONF_UTILITYTYPE, DEFAULT_NAME, DOMAIN, SENSOR, UTILITYGAS, UTILITYWATER
from .entity import MeterParserEntity
from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    ENERGY_KILO_WATT_HOUR,
    VOLUME_CUBIC_METERS,
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([MeterParserSensor(coordinator, entry)])


class MeterParserSensor(MeterParserEntity):
    def __init__(self, coordinator, entry):
        """Initialize the cover."""
        self.coordinator = coordinator
        self.metertype = entry.data.get(CONF_METERTYPE)
        self.utilitytype = entry.data.get(CONF_UTILITYTYPE)

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
