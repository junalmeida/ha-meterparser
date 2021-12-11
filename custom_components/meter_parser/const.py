"""Constants for Meter Parser"""
#    Copyright 2021 Marcos Junior

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

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
ISSUE_URL = "https://github.com/junalmeida/ha-meterparser/issues"
DOMAIN = "meter_parser"
DEFAULT_NAME = DOMAIN
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
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_RECTANGLE = "rectangle"
CONF_ROTATE_ANGLE = "rotate_angle"
CONF_OCR_API_KEY = "ocr_api_key"
# CONF_OCR_API_URL = "ocr_api_url"

CONF_METERTYPE = "meter_type"
METERTYPEDIALS = "dials"
METERTYPEDIGITS = "digits"
METERTYPES = {METERTYPEDIALS: "Dials", METERTYPEDIGITS: "Digits (OCR)"}

CONF_LIGHT_ENTITY_ID = "light_entity_id"

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
