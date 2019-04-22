import time

import requests

from common import log
from ewt import ewt_helper
from ewt.ewt_client import EWTClient
from ewt.usercenter_lib import usercenter

logger = log.getLoggerForEWT()


class EWTWebClient(EWTClient):
    """
    暂不支持登录用户缓存
    """

    def __init__(self, user, password, auto_login):
        self.user = user
        self.password = password
        self.request_session = requests.session()
        self.user_token = ""
        self.__is_logged_in = False
        self.__auto_login = auto_login

    def _login(self):
        if not self.__is_logged_in:
            logger.info("Login as user {}".format(self.user))
            rs, user_token = usercenter.pc_login(self.user, self.password)
            self.request_session = rs
            self.user_token = user_token
            self.__is_logged_in = True

    def _logout(self):
        if self.__is_logged_in:
            usercenter.pc_logout(self.request_session)
            self.__is_logged_in = False
        else:
            logger.info("User {} already logged out".format(self.user))

    def get(self, url, params=None, **kwargs):
        if self.__auto_login:
            self._login()

        headers = {}
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        if params and "_" not in params:
            params["_"] = int(time.time() * 1000)
        response = self.request_session.get(url, params=params, headers=headers, **kwargs)
        ret_json = ewt_helper.check_json_response(response)
        return ret_json

    def post(self, url, data=None, json=None, **kwargs):
        if self.__auto_login:
            self._login()

        headers = {}
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        if data and "_" not in data:
            data["_"] = int(time.time() * 1000)
        response = self.request_session.post(url, data=data, json=json, headers=headers, **kwargs)
        ret_json = ewt_helper.check_json_response(response)
        return ret_json
