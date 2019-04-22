from common import log
from conf import config
from ewt.ewt_client import EWTClient
from ewt.www_lib.www_urls import WWWUrls

logger = log.getLoggerForEWT()
ewt_cfg = config.getEWTConfig()
protocol = ewt_cfg.getProtocol()
www_host = ewt_cfg.getWWWHost()


class WWW(object):
    """
    构造函数中的ewt_client即可以是ewt_web_client，也可以是ewt_app_client，做到同一个接口兼容app/pc端发送的请求
    请求如何发送，由实例化时传入的ewt_client决定，study只用关心接口的参数逻辑，而不用关心请求发送的逻辑
    """

    def __init__(self, ewt_client: EWTClient):
        self.client = ewt_client
        self.url_builder = WWWUrls(protocol, www_host)

    def edit_user_photo(self, src):
        post_data = {"src": src}
        response = self.client.post(self.url_builder.edit_user_photo, data=post_data)
        logger.debug(response)
        return response
