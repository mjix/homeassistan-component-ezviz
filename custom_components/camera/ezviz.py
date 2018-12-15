"""
Support for Ezviz camera.
"""

import time
import logging
import requests
from homeassistant.components.camera import Camera
from ..ezviz import (PY_EZVIZ_GATEWAY)

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the ezviz camera platform."""
    add_entities([
        EzvizCamera(hass, config)
    ])
    return True

class EzvizCamera(Camera):

    def __init__(self, hass, config):
        """Initialize ezviz camera component."""
        super().__init__()
        self._parent = hass
        self.ezvizService = hass.data[PY_EZVIZ_GATEWAY]

        self.deviceSerial = self.ezvizService.deviceSerial

        self._interval_snapshots = 30
        self._last_image = ""
        self._last_snapshot_time = 0

    @property
    def name(self):
        """Return the name of this camera."""
        return self.ezvizService.name

    @property
    def should_poll(self):
        """Camera should poll periodically."""
        return True

    @property
    def motion_detection_enabled(self):
        result = self.ezvizService.post('/lapp/device/info', data={'deviceSerial':self.deviceSerial})
        return result.get('data', {}).get('defence') == 1

    def enable_motion_detection(self):
        result = self.ezvizService.post('/lapp/device/defence/set', data={'deviceSerial':self.deviceSerial,'isDefence': 1})
        self.schedule_update_ha_state()

    def disable_motion_detection(self):
        result = self.ezvizService.post('/lapp/device/defence/set', data={'deviceSerial':self.deviceSerial,'isDefence': 0})
        self.schedule_update_ha_state()

    def camera_image(self):
        """Return a faked still image response."""
        if not self.ezvizService.switchState:
            return ""

        now = time.time()
        if now < self._last_snapshot_time + self._interval_snapshots:
            return self._last_image

        result = self.ezvizService.post('/lapp/device/capture', data={'deviceSerial':self.deviceSerial,'channelNo':1})
        if (result['code']!='200'):
            _LOGGER.error("EZVIZ capture image fail:%s", result)
            return self._last_image

        image_path = result['data']['picUrl']
        try:
            response = requests.get(image_path)
        except requests.exceptions.RequestException as error:
            _LOGGER.error("EZVIZ getting camera image: %s", error)
            return self._last_image

        self._last_snapshot_time = now
        self._last_image = response.content
        return self._last_image
