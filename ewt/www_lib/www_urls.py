class WWWUrls(object):
    def __init__(self, protocol, host):
        self.__protocol = protocol
        self.__host = host
        self.__init_urls()

    def __init_urls(self):
        baseurl = "{}://{}".format(self.__protocol, self.__host)
        self.edit_user_photo = baseurl + "/Ajax/EditPhoto"
