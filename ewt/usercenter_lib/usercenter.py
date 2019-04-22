import json
import time
from urllib import parse

import requests

from common import log, helper
from conf import config
from ewt import ewt_const
from ewt import ewt_helper
from ewt.ewt_client import EWTClient
from ewt.usercenter_lib.usercenter_urls import UCUrls

logger = log.getLoggerForEWT()
ewt_cfg = config.getEWTConfig()
protocol = ewt_cfg.getProtocol()
uc_host = ewt_cfg.getUserCenterHost()
uc_urls = UCUrls(protocol, uc_host)


def pc_login(username, password, sid=2, isremember=1, fromurl="http://www.test.mistong.com/", callback=""):
    # sid含义：2=www,3=study,11=xinli
    aes_password = ewt_helper.encrypt_pc_password(password)
    logger.debug("password is: {}".format(aes_password))
    queries = {"username": username, "password": aes_password, "sid": sid, "isremember": isremember, "fromurl": fromurl}
    if not callback:
        queries["callback"] = callback
    login_session = requests.session()
    response = login_session.post(uc_urls.prelogin, data=queries)
    logger.debug(response.text)
    ret_json = json.loads(response.text)
    if ret_json["code"] != 200:
        logger.fatal("Login failed, response is: {}".format(response.text))
    redirect_url = parse.urlparse(ret_json['data']['url'])
    qs = parse.parse_qs(redirect_url.query)
    user_token = qs['tk']
    return login_session, user_token


def pc_logout(login_session):
    # todo: logout
    return


def app_login(username, password, sid=6, platform=2, devicetoken="", devicename=""):
    sign_switcher = {2: ewt_const.web_sign, 6: ewt_const.android_sign, 7: ewt_const.ios_sign}
    # todo: 当sid=2时，登录报错，提示密码有误
    login_session = requests.session()
    encrypt_password = ewt_helper.encrypt_app_password(password)
    post_data = {"username": username, "password": encrypt_password, "sid": sid, "platform": platform,
                 "devicetoken": devicetoken, "devicename": devicename}
    sign_value = sign_switcher.get(sid)
    post_data['sign'] = helper.get_str_md5(sign_value)
    post_data['timestamp'] = int(time.time() * 1000)

    response = login_session.post(uc_urls.app_login, data=post_data)
    logger.debug(response.text)
    ret_json = ewt_helper.check_json_response(response)
    if "Token" not in ret_json:
        logger.fatal("Login failed, response is: {}".format(response.text))
    login_session.close()
    return ret_json['Token']


def app_logout(user_token):
    # todo: logout is to make the user_token expire
    return


class UserCenter(object):
    def __init__(self, ewt_client: EWTClient):
        """
        做到同一个接口兼容app/pc端发送的请求，由实例化时传入的ewt_client决定如何发请求，study只用关心接口的参数逻辑，而不用关心请求发送的逻辑
        :param ewt_client: 构造函数中的ewt_client即可以是ewt_web_client，也可以是ewt_app_client
        """
        self.client = ewt_client
        self.url_builder = uc_urls

    def verify_is_expired_member(self, callback=""):
        # callback=jQuery111203415133948714606_1537525231661&username=test00003&_=1537525231663
        queries = {"callback": callback, "username": self.client.user}
        response = self.client.get(self.url_builder.verify_is_expired_member, params=queries)
        logger.debug(response)
        return response
