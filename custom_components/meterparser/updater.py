from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import logging

from .const import DOMAIN
from .parser_dial import parse_dials
_LOGGER: logging.Logger = logging.getLogger(__package__)
SCAN_INTERVAL = timedelta(seconds=30)

try:
    # Verify that the OpenCV python package is pre-installed
    import cv2

    CV2_IMPORTED = True
except ImportError:
    CV2_IMPORTED = False


class MeterParserCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data"""

    def __init__(
        self, hass: HomeAssistant, uri: str, metertype: str
    ) -> None:
        """Initialize."""
        self.platforms = []

        self.uri = uri
        self.metertype = metertype

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via opencv."""
        if not CV2_IMPORTED:
            raise UpdateFailed('No OpenCV library found! Install or compile for your system')

        try:
            cap = cv2.VideoCapture(self.uri)
            ret, frame = cap.read()
            return parse_dials(frame, 5)
        except Exception as exception:
            raise UpdateFailed() from exception
        finally:
            try:
                cap.release()
            finally:
                cv2.destroyAllWindows()
