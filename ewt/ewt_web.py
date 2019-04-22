from ewt.ewt_web_client import EWTWebClient
from ewt.study_lib import study
from ewt.usercenter_lib import usercenter
from ewt.www_lib import www


class EWTWeb(object):
    """
    暂不支持登录用户缓存
    """

    def __init__(self, user, password, auto_login=True):
        self.user = user
        self.password = password
        self.auto_login = auto_login
        self.__client = EWTWebClient(self.user, self.password, self.auto_login)
        self.usercenter = usercenter.UserCenter(self.__client)
        self.www = www.WWW(self.__client)
        self.study = study.Study(self.__client)

    def login(self):
        return self.__client._login()

    def logout(self):
        return self.__client._logout()

    def get_user_token(self):
        return self.__client.get_user_token()


if __name__ == '__main__':
    ewt = EWTWeb("test0002", "123456")
    ewt.login()
    print("Web user:{}".format(ewt.get_user_token()))
    v = ewt.usercenter.verify_is_expired_member("q123456789")
    print("response is: {}".format(v))
    assert "q123456789" in v
