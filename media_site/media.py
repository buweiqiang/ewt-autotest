import json
import time
import requests
from media_site.media_urls import MediaUrls
from common import log, helper
from conf import config

cfg = config.getMediaConfig()
logger = log.initLogger("MEDIA", cfg.getLogLevel())


class Media(object):
    """
    meida的接口不需要权限验证，所以不需要登录，用户名和密码都不是必需的
    """

    def __init__(self, user='', password=''):
        self.user = user
        self.password = password
        self.request_session = requests.session()
        self.url_builder = MediaUrls(cfg.getProtocol(), cfg.getHost())

    def get_video_play_url_callback(self, jsonpcallback, videocode, proid=1, plat=1):
        params = {'jsonpcallback': jsonpcallback, 'videocode': videocode, 'proid': proid, 'plat': plat}
        response_text = self.get(self.url_builder.get_video_play_url_callback, params=params)
        return response_text

    def get_video_play_url_list_by_videocode(self, videocode, proid=1, plat=1):
        params = {'videocode': videocode, 'proid': proid, 'plat': plat}
        response_text = self.get(self.url_builder.get_video_play_url_list_by_videocode, params=params)
        return json.loads(response_text)

    def get(self, url, params=None, **kwargs):
        headers = {}
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        if params and "_" not in params:
            params["_"] = int(time.time() * 1000)
        response = self.request_session.get(url, params=params, headers=headers, **kwargs)
        logger.debug(response.text)
        return response.text

    def post(self, url, data=None, json=None, **kwargs):
        headers = {}
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        if data and "_" not in data:
            data["_"] = int(time.time() * 1000)
        response = self.request_session.post(url, data=data, json=json, headers=headers, **kwargs)
        logger.debug(response.text)
        return response.text
