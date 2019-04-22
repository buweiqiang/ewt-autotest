import json
from ewt import ewt_const
from common import helper
from common import log

logger = log.getLoggerForEWT(log.LogType.EWT_COMMON)


def encrypt_pc_password(text, key=ewt_const.WEB_AES_KEY, iv=ewt_const.WEB_AES_IV, block_size=16):
    """
    web登录接口密码加密算法
    :param text: 密码
    :param key: 密钥
    :param iv: 密钥偏移量
    :param block_size: 分组块大小
    :return: 16进制字符串
    """
    encrypt_text = helper.aes_encrypt_cbc(text, key, iv, block_size)
    hex_text = helper.hex_str(encrypt_text)
    return hex_text


def encrypt_app_password(text, key=ewt_const.APP_AES_KEY, block_size=16):
    encrypt_text = helper.aes_encrypt_ecb(text, key, block_size)
    b64encode_text = helper.base64_encode_str(encrypt_text)
    return b64encode_text


def check_json_response(response):
    if response.status_code == 200 and response.content:
        try:
            retJson = json.loads(response.content)
        except ValueError as e:
            logger.warning("Load conetent as json failed: {}".format(e))
        else:
            return retJson
    else:
        # 剩下的情况是：1. response.content为空 2. status_code不为200
        logger.warning("Unexpected response of: %s\n" % response.url)
        if not response.content:
            errorMsg = 'response code is %s, but content is None' % response.status_code
            errorMsg += 'input : ' + response.json()
            errorMsg += 'response : ' + response.content
            logger.warning(errorMsg)
        else:
            errorMsg = 'response status code is: %s\n' % response.status_code
            errorMsg += 'response content: %s' % response.content
            logger.warning(errorMsg)
            # raise AssertionError(errorMsg)
    return response.text
