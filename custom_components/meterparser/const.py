"""Constants for Meter Parser"""

NAME = "Meter Parser Integration"
DOMAIN = "meterparser"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ISSUE_URL = "https://github.com/junalmeida/ha-meterparser/issues"
ATTRIBUTION = "Data provided by xxxx webcam"
# Icons
GAS_ICON = "mdi:fire"
ELETRICITY_ICON = "mdi:lightning"
WATER_ICON = "mdi:water"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_URI = "uri"
CONF_ZOOMFACTOR = "ZOOMFACTOR"
CONF_OCR_API = "OCRKEY"

CONF_METERTYPE = "METERTYPE"
METERTYPEDIALS = "Dials"
METERTYPEDIGITS = "Digits"
METERTYPES = [METERTYPEDIALS, METERTYPEDIGITS]

CONF_AVGSIZE = "DIAL_AVG_SIZE"
CONF_COUNT = "DIAL_COUNT"
CONF_DEBUG = "DEBUG"

CONF_UTILITYTYPE = "ENERGYTYPE"
UTILITYGAS = "Gas"
UTILITYELETRICITY = "Eletricity"
UTILITYWATER = "Water"
UTILITYTYPES = [UTILITYELETRICITY, UTILITYGAS, UTILITYWATER]


DIAL_READOUT_CCW = "CCW"
DIAL_READOUT_CW = "CCW"
DIAL_READOUT_CONVENTIONS = [DIAL_READOUT_CW, DIAL_READOUT_CCW, DIAL_READOUT_CW, DIAL_READOUT_CCW, DIAL_READOUT_CW]

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
