from .const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .entity import MeterParserEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([MeterParserSensor(coordinator, entry)])


class MeterParserSensor(MeterParserEntity):

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON
