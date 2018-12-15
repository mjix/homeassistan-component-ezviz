"""
Support for Ezviz camera.
"""
import logging

from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
from homeassistant.const import (CONF_COMMAND_ON, CONF_COMMAND_OFF)
from ..ezviz import (PY_EZVIZ_GATEWAY)

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the ezviz switch platform."""
    camera = EzvizCamera(hass, config)
    camera.update()
    switches = [camera]
    add_entities(switches)
    return True

class EzvizCamera(SwitchDevice):
    """Representation of a ezviz switch."""

    icon = 'mdi:record-rec'

    def __init__(self, hass, config):
        """Initialize the switch."""
        super().__init__()
        self._parent = hass
        self.ezvizService = hass.data[PY_EZVIZ_GATEWAY]

        self.deviceSerial = self.ezvizService.deviceSerial
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return '{} State'.format(self.ezvizService.name)

    def update(self):
        """Update the switch value."""
        result = self.ezvizService.post('/lapp/device/scene/switch/status', data={'deviceSerial':self.deviceSerial})
        if (result['code']!='200'):
            _LOGGER.info("EZVIZ get switch status fail:%s", result)
            return False
        self._state = result.get('data', {}).get('enable') == 0
        self.ezvizService.switchState = self._state

    @property
    def is_on(self):
        """Return True if entity is on."""
        return self._state

    def _set_switch(self, enable):
        result = self.ezvizService.post('/lapp/device/scene/switch/set', data={'deviceSerial':self.deviceSerial, 'enable':enable})
        _LOGGER.info("EZVIZ set switch:%s", result)
        if (result['code']!='200'):
            return False
        self.schedule_update_ha_state()
        return True

    def turn_on(self, **kwargs):
        """Turn the entity on."""
        self._state = True
        self._set_switch(0)
        

    def turn_off(self, **kwargs):
        """Turn the entity off."""
        self._state = False
        self._set_switch(1)
