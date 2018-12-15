import os
import time
import logging
import requests
import voluptuous as vol
from datetime import timedelta
from homeassistant.helpers.discovery import load_platform
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ezviz'
PY_EZVIZ_GATEWAY = 'ezviz_gw'
API = 'https://open.ys7.com/api'

CONF_ID = 'DeviceId'
CONF_KEY = 'AppKey'
CONF_SEC = 'Secret'
CONF_NAME = 'DeviceName'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_ID): cv.string,
        vol.Required(CONF_KEY): cv.string,
        vol.Required(CONF_SEC): cv.string,
        vol.Required(CONF_NAME): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    hass.data[PY_EZVIZ_GATEWAY] = EzvizService(hass, config[DOMAIN])

    load_platform(hass, 'camera', DOMAIN, {}, config[DOMAIN])
    load_platform(hass, 'switch', DOMAIN, {}, config[DOMAIN])
    return True

class EzvizService():
    """The representation of a Demo camera."""

    def __init__(self, hass, config):
        """Initialize ezviz camera component."""
        super().__init__()
        self._parent = hass
        self.name = config.get(CONF_NAME)
        self.appKey = config.get(CONF_KEY)
        self.appSecret = config.get(CONF_SEC)
        self.accessToken = ""
        self.deviceSerial = config.get(CONF_ID)
        self.expireTime = 0 
        self.switchState = False

    def get_token(self):
        if self.check_token_is_expired():
            self.accessToken = ""

        if self.accessToken:
            return self.accessToken

        r = requests.post(API+'/lapp/token/get', data={'appKey':self.appKey,'appSecret':self.appSecret})
        token_result = r.json()
        if (token_result['code']=='200'):
            self.accessToken = token_result['data']['accessToken']
            self.expireTime = token_result['data']['expireTime']
            return self.accessToken
        else:
            raise Exception("EZVIZ get access token error:%s" % token_result)
        return None

    def check_token_is_expired(self):
        now = int(round(time.time() * 1000))
        if (now > (self.expireTime-1000)):
            return True
        else:
            return False

    def post(self, url, data={}):
        data['accessToken'] = self.get_token()
        r = requests.post(API+url, data)
        result = r.json()
        return result
