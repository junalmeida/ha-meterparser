# from datetime import timedelta
# import datetime
# from config.custom_components.meterparser.config_flow import METERS
# from homeassistant.helpers.entity import DeviceInfo
# from homeassistant.helpers.update_coordinator import UpdateFailed

# # from config.custom_components.meterparser.coordinator import MeterParserCoordinator
# from homeassistant import config_entries, core

# from homeassistant.components.sensor import (
#     PLATFORM_SCHEMA,
#     STATE_CLASS_MEASUREMENT,
#     SensorEntity,
#     SensorEntityDescription,
# )

# from .const import (
#     CONF_AVGSIZE,
#     CONF_COUNT,
#     CONF_DEBUG,
#     CONF_METERTYPE,
#     CONF_ENTITY_ID,
#     CONF_UTILITYTYPE,
#     DEFAULT_NAME,
#     DOMAIN,
#     METERTYPEDIALS,
#     METERTYPEDIGITS,
#     SENSOR,
#     UTILITYELECTRICITY,
#     UTILITYNATURALGAS,
#     UTILITYWATER,
# )
# from homeassistant.const import (
#     DEVICE_CLASS_ENERGY,
#     ENERGY_KILO_WATT_HOUR,
#     VOLUME_CUBIC_METERS,
# )
# from .parser_dial import parse_dials
# from .parser_digits import parse_digits

# try:
#     # Verify that the OpenCV python package is pre-installed
#     import cv2

#     CV2_IMPORTED = True
# except ImportError:
#     CV2_IMPORTED = False

# # Time between updating data from image
# SCAN_INTERVAL = timedelta(minutes=10)


# async def async_setup_entry(
#     hass: core.HomeAssistant,
#     config_entry: config_entries.ConfigEntry,
#     async_add_entities,
# ):
#     """Setup sensor platform."""
#     # coordinator: MeterParserCoordinator = hass.data[DOMAIN][entry.entry_id]
#     for i, item in enumerate(config_entry.data[METERS]):
#         async_add_entities([MeterParserSensor(hass, i + 1, item)])


# class MeterParserSensor(SensorEntity):
#     def __init__(self, hass: core.HomeAssistant, index: int, entry: dict):
#         """Initialize"""
#         super().__init__()

#         self.metertype: str = entry[CONF_METERTYPE]
#         self.utilitytype: str = entry[CONF_UTILITYTYPE]
#         self.uri: str = entry[CONF_ENTITY_ID]
#         self.count = int(entry[CONF_COUNT])
#         self.avgsize = int(entry[CONF_AVGSIZE])
#         self.debug = bool(entry[CONF_DEBUG])
#         self._last_update_success: datetime.datetime = None

#         self._attr_should_poll = True
#         self._attr_assumed_state = False

#         if index > 1:
#             name = "%s Reading %d" % (self.utilitytype.capitalize(), index)
#         else:
#             name = "%s Reading" % self.utilitytype.capitalize()

#         self._attr_unique_id = "%s_reading_%d" % (self.utilitytype.lower(), index)
#         if self.utilitytype == UTILITYNATURALGAS:
#             unit_of_measurement = "m3"
#         elif self.utilitytype == UTILITYWATER:
#             unit_of_measurement = "m3"
#         elif self.utilitytype == UTILITYELECTRICITY:
#             unit_of_measurement = "kW"

#         if self.utilitytype == UTILITYNATURALGAS:
#             icon = "mdi:fire"
#         elif self.utilitytype == UTILITYWATER:
#             icon = "mdi:water"
#         else:
#             icon = "mdi:lightning-bolt"

#         self.entity_description = SensorEntityDescription(
#             key=self._attr_unique_id,
#             name=name,
#             native_unit_of_measurement=unit_of_measurement,
#             state_class=STATE_CLASS_MEASUREMENT,
#             device_class=DEVICE_CLASS_ENERGY,
#             icon=icon,
#         )

#         self._attr_device_info = {
#             "uri": self.uri,
#             "meter_type": self.metertype,
#             "utility": self.utilitytype,
#         }  # TODO: Replace with DeviceInfo typed dict

#     @property
#     def available(self):
#         """Return if entity is available."""
#         if self._last_update_success is None:
#             return False
#         delta = datetime.datetime.now() - self._last_update_success
#         return delta.total_seconds < SCAN_INTERVAL.total_seconds + 120

#     def update(self):
#         """Update data via opencv."""
#         if not CV2_IMPORTED:
#             raise UpdateFailed(
#                 "No OpenCV library found! Install or compile for your system"
#             )

#         try:
#             cap = cv2.VideoCapture(self.uri)
#             _, frame = cap.read()
#             if self.metertype == METERTYPEDIALS:
#                 self._attr_native_value = parse_dials(
#                     frame,
#                     minDiameter=self.avgsize,
#                     maxDiameter=self.avgsize + 100,
#                     debug=self.debug,
#                 )
#             elif self.metertype == METERTYPEDIGITS:
#                 self._attr_native_value = parse_digits(frame, self.count, self.debug)

#             self._last_update_success = datetime.datetime.now()
#         except Exception as exception:
#             raise UpdateFailed() from exception
#         finally:
#             try:
#                 cap.release()
#             finally:
#                 cv2.destroyAllWindows()
