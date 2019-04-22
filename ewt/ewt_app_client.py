import requests

from common import log, helper
from ewt import ewt_const
from ewt import ewt_helper
from ewt.ewt_client import EWTClient
from ewt.ewt_const import APP_AES_KEY as sign_key
from ewt.ewt_const import RequestSignMode
from ewt.usercenter_lib import usercenter

logger = log.getLoggerForEWT(log.LogType.EWT_APP)


class EWTAppClient(EWTClient):
    def __init__(self, user, password, sid, auto_login):
        self.user = user
        self.password = password
        self.sid = sid
        self.request_session = requests.session()
        self.user_token = ""
        self.__is_logged_in = False
        self.__auto_login = auto_login
        self.os_version = ''

    def _login(self):
        if not self.__is_logged_in:
            logger.info("Login as user {}".format(self.user))
            user_token = usercenter.app_login(self.user, self.password, self.sid)
            self.user_token = user_token
            self.userid = int(user_token.split('-')[0])
            self.__userid = int(ewt_const.userid_keybin ^ self.userid)
            self.__is_logged_in = True

    def _logout(self):
        if self.__is_logged_in:
            usercenter.app_logout(self.user_token)
            self.__is_logged_in = False
        else:
            logger.info("User {} already logged out".format(self.user))

    def set_os_version(self, os_version):
        self.os_version = os_version

    def __get_request_header(self):
        headers = {"userid": str(self.__userid)}
        return headers

    def __append_request_params(self, origin_params, sign_mode=RequestSignMode.no_token_no_sort_key_value_list):
        """
        补充请求参数
        :param origin_params: 原始参数，即从通过用户选择传过来的参数
        :param sign_mode: 加签的模式
        :return: 补充完参数后的字典
        """
        exclude_keys = ['sid', 'osVersion', 'token']
        prepared_params = {}
        if not origin_params:
            origin_params = {}

        prepared_params.update(origin_params)
        # add token to request body
        prepared_params["token"] = self.user_token

        # add sign to request body
        if not 'sign' in prepared_params:
            _content = ''
            # 1. 开头加key
            _content += sign_key
            # 2. 中间加参数值列表
            value_list_for_sign = []
            keys = [k for k in prepared_params.keys() if k not in exclude_keys]
            # sign_mode > 10 表示签名时要包含token
            if sign_mode > 10:
                keys.append('token')

            if sign_mode % 10 == 1:
                # 1 先按照key进行排序，再拼接value后进行签名
                value_list_for_sign = [prepared_params[k] for k in sorted(keys)]
            elif sign_mode % 10 == 2:
                # 2 先按照key进行排序，再按照key=value的格式拼接后进行签名
                value_list_for_sign = ["&{}={}".format(k, prepared_params[k]) for k in sorted(keys)]
            elif sign_mode % 10 == 3:
                # 3 不排序，按原顺序拼接value后进行签名
                value_list_for_sign = [prepared_params[k] for k in keys]
            elif sign_mode % 10 == 4:
                # 4 不排序，按原顺序，按照key=value的格式拼接后进行签名
                value_list_for_sign = ["&{}={}".format(k, prepared_params[k]) for k in keys]

            for v in value_list_for_sign:
                _content += str(v)
            # 3. 结尾加上key
            if sign_mode % 2 == 0:
                _content += "&" + sign_key
            else:
                _content += sign_key
            # 4. 获取md5签名
            prepared_params["sign"] = helper.get_str_md5(_content)

        # add sid in request body
        if not 'sid' in prepared_params:
            prepared_params['sid'] = self.sid

        # add sid in request body
        if not 'osVersion' in prepared_params:
            prepared_params['osVersion'] = self.os_version

        return prepared_params

    def get(self, url, params=None, **kwargs):
        return self.__send_request('get', url, params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.__send_request('post', url, data, json, **kwargs)

    def __send_request(self, method: str, url: str, params=None, json=None, **kwargs):
        if self.__auto_login:
            self._login()

        headers = self.__get_request_header()
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        retry_for_sign_mode = True
        if params and 'sign' in params:
            retry_for_sign_mode = False

        # 尝试不同的加签模式进行签名并发送请求，遇到签名验证通过的结果即返回
        for sm in RequestSignMode.all_sign_modes():
            params_prepared = self.__append_request_params(params, sign_mode=sm)
            if 'get' == method.lower():
                response = self.request_session.get(url, params=params_prepared, headers=headers, **kwargs)
            else:
                response = self.request_session.post(url, data=params_prepared, json=json, headers=headers, **kwargs)
            ret_json = ewt_helper.check_json_response(response)
            # 如果不需要重试，直接退出循环
            if not retry_for_sign_mode:
                break
            # 如果返回的结果是签名验证失败（703），则继续循环尝试采用不同的签名方式进行验证，否则退出循环
            if 'code' in ret_json and ret_json['code'] == 703:
                continue
            else:
                break
        return ret_json
