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
CONF_ZOOMFACTOR = "zoom_factor"
CONF_OCR_API = "ocr_key"

CONF_METERTYPE = "meter_type"
METERTYPEDIALS = "DIALS"
METERTYPEDIGITS = "DIGITS"
METERTYPES = {METERTYPEDIALS: "Dials", METERTYPEDIGITS: "Digits (OCR)"}

CONF_AVGSIZE = "dial_avg"
CONF_COUNT = "dial_count"
CONF_DEBUG = "debug"

CONF_UTILITYTYPE = "utility_type"
UTILITYGAS = "GAS"
UTILITYELETRICITY = "ELETRICITY"
UTILITYWATER = "WATER"
UTILITYTYPES = {
    UTILITYELETRICITY: "Eletricity",
    UTILITYGAS: "Gas",
    UTILITYWATER: "Water",
}


DIAL_READOUT_CCW = "CCW"
DIAL_READOUT_CW = "CCW"
DIAL_READOUT_CONVENTIONS = [
    DIAL_READOUT_CW,
    DIAL_READOUT_CCW,
    DIAL_READOUT_CW,
    DIAL_READOUT_CCW,
    DIAL_READOUT_CW,
]
READING = "reading"

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
