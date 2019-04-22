import abc
import requests


class EWTClient(metaclass=abc.ABCMeta):
    def __init__(self, user, password, auto_login):
        self.user = user
        self.password = password
        self.request_session = requests.session()
        self.user_token = ""
        self.__is_logged_in = False
        self.__auto_login = auto_login

    @abc.abstractmethod
    def _login(self):
        pass

    @abc.abstractmethod
    def _logout(self):
        pass

    @abc.abstractmethod
    def get(self, url, params=None, **kwargs):
        pass

    @abc.abstractmethod
    def post(self, url, data=None, json=None, **kwargs):
        pass

    def get_user_token(self):
        self._login()
        return self.user_token
