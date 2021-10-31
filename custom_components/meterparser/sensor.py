from datetime import timedelta
import datetime
from homeassistant.helpers.update_coordinator import UpdateFailed

# from config.custom_components.meterparser.coordinator import MeterParserCoordinator
from homeassistant import config_entries, core
from .const import (
    CONF_AVGSIZE,
    CONF_COUNT,
    CONF_DEBUG,
    CONF_METERTYPE,
    CONF_URI,
    CONF_UTILITYTYPE,
    DEFAULT_NAME,
    DOMAIN,
    METERTYPEDIALS,
    METERTYPEDIGITS,
    SENSOR,
    UTILITYELETRICITY,
    UTILITYGAS,
    UTILITYWATER,
)
from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    ENERGY_KILO_WATT_HOUR,
    VOLUME_CUBIC_METERS,
)
from parser_dial import parse_dials
from parser_digits import parse_digits

try:
    # Verify that the OpenCV python package is pre-installed
    import cv2

    CV2_IMPORTED = True
except ImportError:
    CV2_IMPORTED = False

# Time between updating data from image
SCAN_INTERVAL = timedelta(minutes=10)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensor platform."""
    # coordinator: MeterParserCoordinator = hass.data[DOMAIN][entry.entry_id]
    for item in config_entry.data:
        async_add_entities([MeterParserSensor(hass, item)])


class MeterParserSensor(config_entries.EntityRegistryDisabledHandler):
    def __init__(self, hass: core.HomeAssistant, entry):
        """Initialize"""
        super().__init__(hass)
        self.metertype = entry[CONF_METERTYPE]
        self.utilitytype = entry[CONF_UTILITYTYPE]
        self.uri = entry[CONF_URI]
        self.count = entry[CONF_COUNT]
        self.avgsize = entry[CONF_AVGSIZE]
        self.debug = entry[CONF_DEBUG]
        self._last_reading = None
        self._last_update_success = None
        if self.utilitytype == UTILITYGAS:
            self._unit_of_measurement = "m3"
        elif self.utilitytype == UTILITYWATER:
            self._unit_of_measurement = "m3"
        elif self.utilitytype == UTILITYELETRICITY:
            self._unit_of_measurement = "kW"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.utilitytype}_reading"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._last_reading

    @property
    def device_class(self):
        """Return device class"""
        return DEVICE_CLASS_ENERGY

    @property
    def device_info(self):
        """Return device_info for device registry."""
        return {
            "uri": self.uri,
            "meter type": self.metertype,
            "utility": self.utilitytype,
        }

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self.utilitytype == UTILITYGAS:
            return "mdi:fire"
        elif self.utilitytype == UTILITYWATER:
            return "mdi:water"
        else:
            return "mdi:lightning"

    @property
    def should_poll(self):
        """This device requires pooling"""
        return True

    @property
    def available(self):
        """Return if entity is available."""
        return self._last_update_success is not None

    @property
    def unit_of_measurement(self):
        """Unity of measurement based on utility type"""
        return self._unit_of_measurement

    async def async_update(self):
        """Update data via opencv."""
        if not CV2_IMPORTED:
            raise UpdateFailed(
                "No OpenCV library found! Install or compile for your system"
            )

        try:
            cap = cv2.VideoCapture(self.uri)
            _, frame = cap.read()
            if self.metertype == METERTYPEDIALS:
                self._last_read = parse_dials(
                    frame,
                    minDiameter=self.avgsize,
                    maxDiameter=self.avgsize + 100,
                    debug=self.debug,
                )
            elif self.metertype == METERTYPEDIGITS:
                self._last_read = parse_digits(frame, self.count, self.debug)

            self._last_update_success = datetime.datetime.now()
        except Exception as exception:
            raise UpdateFailed() from exception
        finally:
            try:
                cap.release()
            finally:
                cv2.destroyAllWindows()
