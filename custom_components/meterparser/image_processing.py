"""Meter Parser Image Processing component"""
import datetime
import logging
import os
import numpy
import voluptuous as vol

from .parser_dial import parse_dials
from .parser_digits import parse_digits

from homeassistant.components.image_processing import (
    CONF_ENTITY_ID,
    CONF_NAME,
    PLATFORM_SCHEMA,
    ImageProcessingEntity,
)
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_UNIT_OF_MEASUREMENT,
    DEVICE_CLASS_GAS,
    DEVICE_CLASS_POWER,
    POWER_KILO_WATT,
)
from homeassistant.core import Config, HomeAssistant, callback, split_entity_id
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import device_registry as dr
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import (
    EntityDescription,
    generate_entity_id,
)

from .const import (
    ALLOWED_DEVICE_CLASSES,
    CONF_DEBUG,
    CONF_DECIMALS_COUNT,
    CONF_DIAL_SIZE,
    CONF_DIALS,
    CONF_DIGITS_COUNT,
    CONF_METERTYPE,
    CONF_OCR_API,
    CONF_ZOOMFACTOR,
    DEVICE_CLASS_WATER,
    DIAL_DEFAULT_READOUT,
    DOMAIN,
    ICON_ELECTRICITY,
    ICON_GAS,
    ICON_WATER,
    METERTYPEDIALS,
    METERTYPEDIGITS,
    METERTYPES,
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME): cv.string,
        vol.Required(CONF_ENTITY_ID): cv.entity_domain("camera"),
        vol.Optional(CONF_ZOOMFACTOR, default=1): cv.positive_int,
        vol.Required(CONF_METERTYPE): vol.In(METERTYPES),
        vol.Optional(CONF_OCR_API): cv.string,
        vol.Optional(CONF_DIGITS_COUNT, default=6): cv.positive_int,
        vol.Optional(CONF_DECIMALS_COUNT, default=0): cv.positive_int,
        vol.Optional(CONF_DEBUG, default=False): cv.boolean,
        vol.Required(CONF_DEVICE_CLASS): vol.In(ALLOWED_DEVICE_CLASSES),
        vol.Required(CONF_UNIT_OF_MEASUREMENT): cv.string,
        vol.Optional(CONF_DIALS): cv.ensure_list,
        vol.Optional(CONF_DIAL_SIZE, default=100): cv.positive_int,
    }
)

try:
    # Verify that the OpenCV python package is pre-installed
    import cv2

    CV2_IMPORTED = True
except ImportError:
    CV2_IMPORTED = False

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_platform(
    hass: HomeAssistant, config: dict, async_add_entities, discovery_info=None
):
    """Set up the Meter Parser platform."""
    """Set up the OpenCV image processing platform."""
    if not CV2_IMPORTED:
        _LOGGER.error(
            "No OpenCV library found! Install or compile for your system "
            "following instructions here: http://opencv.org/releases.html"
        )
        return

    entities = []
    entities.append(MeterParserMeasurementEntity(hass, config))
    # TODO: Add other entities

    async_add_entities(entities)


class MeterParserMeasurementEntity(ImageProcessingEntity):
    """Measurement entity."""

    def __init__(self, hass: HomeAssistant, config: dict):
        """Initialize."""
        super().__init__()
        self._confidence = 0.7
        self._camera = config[CONF_ENTITY_ID]
        self._debug: bool = bool(config[CONF_DEBUG] if CONF_DEBUG in config else False)
        self._debug_path = hass.config.path("debug/" + DOMAIN) if self._debug else None
        if self._debug_path is not None and not os.path.exists(self._debug_path):
            os.makedirs(self._debug_path)
        name = config[CONF_NAME]
        if name is None or name == "":
            registry = er.async_get(hass)
            entry = registry.async_get(self._camera)
            name = entry.name
        self._attr_unique_id = generate_entity_id(
            "sensor.{}_measurement", name, None, hass
        )
        self.entity_description = EntityDescription(
            key="measurement",
            name=name,
            device_class=config[CONF_DEVICE_CLASS]
            if CONF_DEVICE_CLASS in config
            else DEVICE_CLASS_POWER,
            unit_of_measurement=config[CONF_UNIT_OF_MEASUREMENT]
            if CONF_UNIT_OF_MEASUREMENT in config
            else POWER_KILO_WATT,
        )
        if self.entity_description.device_class == DEVICE_CLASS_POWER:
            self.entity_description.icon = ICON_ELECTRICITY
        elif self.entity_description.device_class == DEVICE_CLASS_GAS:
            self.entity_description.icon = ICON_GAS
        elif self.entity_description.device_class == DEVICE_CLASS_WATER:
            self.entity_description.icon = ICON_WATER

        if name:
            self._attr_name = name
        else:
            self._attr_name = f"Unnamed Meter {split_entity_id(self._camera)[1]}"
        self._metertype: str = (
            config[CONF_METERTYPE] if CONF_METERTYPE in config else METERTYPEDIALS
        )
        self._dials: list[str] = (
            config[CONF_DIALS] if CONF_DIALS in config else DIAL_DEFAULT_READOUT
        )
        self._dial_size = int(
            config[CONF_DIAL_SIZE] if CONF_DIAL_SIZE in config else 100
        )
        self._digits: int = int(
            config[CONF_DIGITS_COUNT] if CONF_DIGITS_COUNT in config else 0
        )
        self._decimals: int = int(
            config[CONF_DECIMALS_COUNT] if CONF_DECIMALS_COUNT in config else 0
        )
        self._ocr_key: str = config[CONF_OCR_API] if CONF_OCR_API in config else ""

        self._attr_extra_state_attributes = {CONF_METERTYPE: self._metertype}

    @property
    def confidence(self):
        """Return minimum confidence for send events."""
        return self._confidence

    @property
    def camera_entity(self):
        """Return camera entity id from process pictures."""
        return self._camera

    async def async_process_image(self, image):
        """Process image."""
        """Update data via opencv."""
        cv_image = cv2.imdecode(numpy.asarray(bytearray(image)), cv2.IMREAD_UNCHANGED)
        reading = 0
        if self._metertype == METERTYPEDIALS:
            reading = parse_dials(
                cv_image,
                readout=self._dials,
                minDiameter=self._dial_size,
                maxDiameter=self._dial_size + 100,
                debug_path=self._debug_path,
            )
        elif self._metertype == METERTYPEDIGITS:
            reading = parse_digits(
                cv_image, self._digits, self._ocr_key, debug_path=self._debug_path
            )
        if self._decimals > 0:
            reading = float(reading) / float(10 ** self._decimals)
        self._attr_state = reading
        self._last_update_success = datetime.datetime.now()
