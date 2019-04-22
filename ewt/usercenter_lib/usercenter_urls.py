class UCUrls(object):
    def __init__(self, protocol, host):
        self.__protocol = protocol
        self.__host = host
        self.__init_urls()

    def __init_urls(self):
        baseurl = "{}://{}".format(self.__protocol, self.__host)
        self.prelogin = baseurl + "/login/prelogin"
        self.get_user = baseurl + "/Ajax/GetUser"
        self.app_login = baseurl + "/apimember/login"
        self.verify_is_expired_member = baseurl + "/Login/VerifyIsExpiredMember"
