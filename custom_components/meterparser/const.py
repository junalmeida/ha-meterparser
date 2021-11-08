"""Constants for Meter Parser"""

from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_GAS,
    DEVICE_CLASS_POWER,
    ENERGY_KILO_WATT_HOUR,
    ENERGY_MEGA_WATT_HOUR,
    ENERGY_WATT_HOUR,
    VOLUME_CUBIC_FEET,
    VOLUME_CUBIC_METERS,
    VOLUME_GALLONS,
    VOLUME_LITERS,
)


NAME = "Meter Parser Integration"
# DOMAIN = "meterparser"
# DOMAIN_DATA = f"{DOMAIN}_data"
# VERSION = "0.0.1"
ISSUE_URL = "https://github.com/junalmeida/ha-meterparser/issues"
ATTRIBUTION = "Data provided by %s camera"
# Icons
ICON_GAS = "mdi:fire"
ICON_ELECTRICITY = "mdi:lightning-bolt"
ICON_WATER = "mdi:water"
DEVICE_CLASS_WATER = "water"
ALLOWED_DEVICE_CLASSES = {
    DEVICE_CLASS_POWER: "Electricity",
    DEVICE_CLASS_ENERGY: "Electricity",
    DEVICE_CLASS_GAS: "Natural Gas",
    DEVICE_CLASS_WATER: "Water",
}
UNITS_OF_MEASUREMENT = {
    VOLUME_CUBIC_METERS,
    VOLUME_CUBIC_FEET,
    ENERGY_KILO_WATT_HOUR,
    ENERGY_MEGA_WATT_HOUR,
    ENERGY_WATT_HOUR,
    VOLUME_GALLONS,
    VOLUME_LITERS,
}

# # Platforms
# SENSOR = "sensor"
# PLATFORMS = [SENSOR]

# Configuration and options
# CONF_ENTITY_ID = "entity_id"
CONF_ZOOMFACTOR = "zoom_factor"
CONF_OCR_API = "ocr_space_key"

CONF_METERTYPE = "meter_type"
METERTYPEDIALS = "dials"
METERTYPEDIGITS = "digits"
METERTYPES = {METERTYPEDIALS: "Dials", METERTYPEDIGITS: "Digits (OCR)"}

CONF_DIAL_SIZE = "dial_size"
CONF_DIGITS_COUNT = "digits"
CONF_DECIMALS_COUNT = "decimals"
CONF_DIALS = "dials"  # This is the readout convention
CONF_DEBUG = "debug"

DIAL_READOUT_CCW = "CCW"
DIAL_READOUT_CW = "CW"
DIAL_DEFAULT_READOUT = [
    DIAL_READOUT_CCW,
    DIAL_READOUT_CW,
    DIAL_READOUT_CCW,
    DIAL_READOUT_CW,
]

READING = "reading"

# # Defaults
DOMAIN = "meter_parser"
DEFAULT_NAME = DOMAIN


# STARTUP_MESSAGE = f"""
# -------------------------------------------------------------------
# {NAME}
# Version: {VERSION}
# This is a custom integration!
# If you have any issues with this you need to open an issue here:
# {ISSUE_URL}
# -------------------------------------------------------------------
# """
