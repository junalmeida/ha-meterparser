"""Meter Parser Image Processing component and sensor."""
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

import asyncio
import datetime
import logging
import os
import numpy
import voluptuous as vol


from homeassistant.components.sensor import (
    STATE_CLASS_TOTAL_INCREASING,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import slugify

from .parser_dial import parse_dials
from .parser_digits import parse_digits

from homeassistant.components.image_processing import (
    CONF_ENTITY_ID,
    CONF_NAME,
    PLATFORM_SCHEMA,
    ImageProcessingEntity,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_DEVICE_CLASS,
    CONF_SOURCE,
    CONF_UNIT_OF_MEASUREMENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_GAS,
    DEVICE_CLASS_POWER,
    ENERGY_KILO_WATT_HOUR,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)
from homeassistant.components.light import (
    DOMAIN as DOMAIN_LIGHT,
)
from homeassistant.components.camera import (
    DOMAIN as DOMAIN_CAMERA,
    ENTITY_ID_FORMAT,
)

from homeassistant.core import HomeAssistant, callback, split_entity_id
from homeassistant.helpers import entity_registry as er
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import (
    generate_entity_id,
)
from homeassistant.helpers.event import async_call_later

from .const import (
    ALLOWED_DEVICE_CLASSES,
    ATTRIBUTION,
    CONF_DEBUG,
    CONF_DECIMALS_COUNT,
    CONF_DIAL_SIZE,
    CONF_DIALS,
    CONF_DIGITS_COUNT,
    CONF_METERTYPE,
    CONF_OCR_API_KEY,
    CONF_RECTANGLE,
    CONF_ROTATE_ANGLE,
    DEVICE_CLASS_WATER,
    DIAL_DEFAULT_READOUT,
    DOMAIN,
    ICON_ELECTRICITY,
    ICON_GAS,
    ICON_WATER,
    METERTYPEDIALS,
    METERTYPEDIGITS,
    METERTYPES,
    UNITS_OF_MEASUREMENT,
    CONF_LIGHT_ENTITY_ID,
)

SOURCE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): cv.entity_domain(DOMAIN_CAMERA),
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_LIGHT_ENTITY_ID): cv.entity_domain(DOMAIN_LIGHT),
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SOURCE): vol.All(cv.ensure_list, [SOURCE_SCHEMA]),
        vol.Optional(CONF_RECTANGLE, default=None): cv.ensure_list,
        vol.Optional(CONF_ROTATE_ANGLE, default=0): vol.All(
            int, vol.Range(min=-360, max=360)
        ),
        vol.Required(CONF_METERTYPE): vol.In(METERTYPES),
        # vol.Optional(CONF_OCR_API_URL): cv.string,
        vol.Optional(CONF_OCR_API_KEY): cv.string,
        vol.Optional(CONF_DIGITS_COUNT, default=6): cv.positive_int,
        vol.Optional(CONF_DECIMALS_COUNT, default=0): cv.positive_int,
        vol.Optional(CONF_DEBUG, default=False): cv.boolean,
        vol.Required(CONF_DEVICE_CLASS): vol.In(ALLOWED_DEVICE_CLASSES),
        vol.Required(CONF_UNIT_OF_MEASUREMENT): vol.In(UNITS_OF_MEASUREMENT),
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
    if not CV2_IMPORTED:
        _LOGGER.error(
            "No OpenCV library found! Install or compile for your system "
            "following instructions here: http://opencv.org/releases.html"
        )
        return

    entities = []
    for camera in config[CONF_SOURCE]:
        entities.append(
            MeterParserMeasurementEntity(
                hass,
                config,
                camera.get(CONF_ENTITY_ID),
                camera.get(CONF_LIGHT_ENTITY_ID),
                camera.get(CONF_NAME),
            )
        )
    async_add_entities(entities)


class MeterParserMeasurementEntity(ImageProcessingEntity, SensorEntity, RestoreEntity):
    """Measurement entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: dict,
        entity_id: str,
        light_entity_id: str,
        entity_name: str,
    ):
        """Initialize."""
        super().__init__()
        self.hass = hass

        hass.bus.async_listen("esphome.device_alive", self._handle_event)

        self._confidence = 0.7
        self._camera = entity_id
        self._light = light_entity_id
        self._debug: bool = bool(config[CONF_DEBUG] if CONF_DEBUG in config else False)
        self._debug_path = hass.config.path("debug/" + DOMAIN) if self._debug else None
        if self._debug_path is not None and not os.path.exists(self._debug_path):
            os.makedirs(self._debug_path)

        if entity_name:
            self._attr_name = entity_name
        else:
            self._attr_name = f"Unnamed Meter {split_entity_id(self._camera)[1]}"

        self._attr_unique_id = generate_entity_id(
            "sensor.{}_" + STATE_CLASS_TOTAL_INCREASING,
            self._attr_name,
            hass=hass,
        )

        device_class = (
            config[CONF_DEVICE_CLASS]
            if CONF_DEVICE_CLASS in config
            else DEVICE_CLASS_POWER
        )

        self.entity_description = SensorEntityDescription(
            key=STATE_CLASS_TOTAL_INCREASING,
            name=self._attr_name,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            device_class=device_class,
            native_unit_of_measurement=config[CONF_UNIT_OF_MEASUREMENT]
            if CONF_UNIT_OF_MEASUREMENT in config
            else ENERGY_KILO_WATT_HOUR,
        )
        if device_class == DEVICE_CLASS_POWER or device_class == DEVICE_CLASS_ENERGY:
            self.entity_description.icon = ICON_ELECTRICITY
        elif device_class == DEVICE_CLASS_GAS:
            self.entity_description.icon = ICON_GAS
        elif device_class == DEVICE_CLASS_WATER:
            self.entity_description.icon = ICON_WATER

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
        self._rect: list[int] = (
            config[CONF_RECTANGLE] if CONF_RECTANGLE in config else None
        )
        self._rotate = (
            int(config[CONF_ROTATE_ANGLE]) if CONF_ROTATE_ANGLE in config else 0
        )
        self._ocr_key: str = (
            config[CONF_OCR_API_KEY] if CONF_OCR_API_KEY in config else ""
        )
        # self._ocr_url: str = (
        #     config[CONF_OCR_API_URL] if CONF_OCR_API_URL in config else ""
        # )

        self._last_update_success: datetime = None
        self._attr_extra_state_attributes = {CONF_METERTYPE: self._metertype}

    @property
    def confidence(self):
        """Return minimum confidence for send events."""
        return self._confidence

    @property
    def camera_entity(self):
        """Return camera entity id from process pictures."""
        return self._camera

    def _handle_event(self, event):
        device_id = ENTITY_ID_FORMAT.format(slugify(event.data.get("device_name")))
        _LOGGER.debug("Got esphome.device_alive event for %s" % device_id)
        if self._camera == device_id:
            asyncio.run_coroutine_threadsafe(self.async_update(), self.hass.loop)
            return

    async def async_update(self):
        """First turn the led on to grab an image"""
        if self._light is not None:
            _LOGGER.debug("Turning on %s" % self._light)
            await self.hass.services.async_call(
                DOMAIN_LIGHT,
                SERVICE_TURN_ON,
                {ATTR_ENTITY_ID: self._light},
            )

            @callback
            async def call_later(*_):
                try:
                    await super(MeterParserMeasurementEntity, self).async_update()
                finally:
                    _LOGGER.debug("Turning off %s" % self._light)
                    await self.hass.services.async_call(
                        DOMAIN_LIGHT,
                        SERVICE_TURN_OFF,
                        {ATTR_ENTITY_ID: self._light},
                    )

            async_call_later(self.hass, 1.5, call_later)
        else:
            await super(MeterParserMeasurementEntity, self).async_update()

    async def async_process_image(self, image):
        """Process image."""
        await self.hass.async_add_executor_job(self.process_image, image)
        if self._attr_attribution is None:
            registry = er.async_get(self.hass)
            entry = registry.entities.get(self._camera)
            self._attr_attribution = ATTRIBUTION % (
                entry.name if entry is not None else split_entity_id(self._camera)[1]
            )

    def process_image(self, image):
        """Update data via opencv."""
        cv_image = cv2.imdecode(numpy.asarray(bytearray(image)), cv2.IMREAD_UNCHANGED)
        if self._rotate != 0:
            cv_image = _rotate_image(image=cv_image, angle=self._rotate)
        if self._rect is not None and len(self._rect) == 4:
            cv_image = _crop_image(image=cv_image, rect=self._rect)

        reading = 0
        if self._metertype == METERTYPEDIALS:
            reading = parse_dials(
                cv_image,
                readout=self._dials,
                entity_id=self._attr_unique_id,
                minDiameter=self._dial_size,
                maxDiameter=self._dial_size + 250,
                debug_path=self._debug_path,
            )
        elif self._metertype == METERTYPEDIGITS:
            reading = parse_digits(
                cv_image,
                self._digits,
                self._ocr_key,
                # self._ocr_url,
                self._attr_unique_id,
                debug_path=self._debug_path,
            )
        if self._decimals > 0:
            reading = float(reading) / float(10 ** self._decimals)
        self._attr_state = float(reading)
        self._attr_native_value = float(reading)
        self._last_update_success = datetime.datetime.now()


def _rotate_image(image, angle, center=None, scale=1.0):
    # grab the dimensions of the image
    (h, w) = image.shape[:2]

    # if the center is None, initialize it as the center of
    # the image
    if center is None:
        center = (w // 2, h // 2)

    # perform the rotation
    M = cv2.getRotationMatrix2D(center, -angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    # return the rotated image
    return rotated


def _crop_image(image, rect):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    return image[y: y + h, x: x + w]
