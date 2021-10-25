"""Constants for Meter Parser"""
# Base component constants
from homeassistant.const import (
    DEVICE_CLASS_GAS,
    DEVICE_CLASS_POWER,
    POWER_KILO_WATT,
    VOLUME_CUBIC_METERS,
)
from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    SensorEntityDescription,
)

from dataclasses import dataclass


NAME = "Meter Parser Integration"
DOMAIN = "meterparser"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ISSUE_URL = "https://github.com/junalmeida/ha-meterparser/issues"
ATTRIBUTION = "Data provided by xxxx webcam"
# Icons
ICON = "mdi:format-quote-close"

# Device classes
SENSOR_DEVICE_CLASS = "energy"  # ??

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_URI = "uri"
CONF_ENERGY = "ENERGY"
CONF_METERTYPE = "METERTYPE"

METERTYPEDIALS = "Dials"
METERTYPEDIGITS = "Digits"
METERTYPES = [METERTYPEDIALS, METERTYPEDIGITS]

ENERGYGAS = "Gas"
ENERGYPOWER = "Power"
ENERGYWATER = "Water"
ENERGYTYPES = [ENERGYPOWER, ENERGYGAS, ENERGYWATER]

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""


@dataclass
class MeterParserSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for Meter Parser."""


SENSORS: tuple[MeterParserSensorEntityDescription, ...] = (
    MeterParserSensorEntityDescription(
        key="meterparser/powerusage",
        name="Current power usage",
        device_class=DEVICE_CLASS_POWER,
        native_unit_of_measurement=POWER_KILO_WATT,
        state_class=STATE_CLASS_MEASUREMENT,
        icon="mdi:mdi-lightning-bolt"
    ),
    MeterParserSensorEntityDescription(
        key="meterparser/gasusage",
        name="Current gas usage",
        device_class=DEVICE_CLASS_GAS,
        icon="mdi:fire",
        native_unit_of_measurement=VOLUME_CUBIC_METERS,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    MeterParserSensorEntityDescription(
        key="meterparser/waterusage",
        name="Current water usage",
        # device_class=DEVICE_CLASS_WATER,
        icon="mdi:water",
        native_unit_of_measurement=VOLUME_CUBIC_METERS,
        state_class=STATE_CLASS_MEASUREMENT,
    )
)
