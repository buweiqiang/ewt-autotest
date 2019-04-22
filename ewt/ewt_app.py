from ewt.ewt_app_client import EWTAppClient
from ewt.study_lib import study
from ewt.usercenter_lib import usercenter


class EWTApp(object):
    def __init__(self, user, password, sid=6, auto_login=True):
        self.user = user
        self.password = password
        self.sid = sid
        self.auto_login = auto_login
        self.__client = EWTAppClient(self.user, self.password, self.sid, self.auto_login)
        self.usercenter = usercenter.UserCenter(self.__client)
        self.study = study.Study(self.__client)
        self.os_version = ''

    def login(self):
        return self.__client._login()

    def logout(self):
        return self.__client._logout()

    def get_user_token(self):
        return self.__client.get_user_token()

    def set_os_version(self, os_version):
        self.os_version = os_version
        self.__client.set_os_version(self.os_version)


if __name__ == '__main__':
    ewt = EWTApp("test0002", "123456")
    ewt.login()
    print("App user: {}".format(ewt.get_user_token()))
