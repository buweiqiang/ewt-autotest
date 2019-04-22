class MediaUrls(object):
    def __init__(self, protocol, host):
        self.__protocol = protocol
        self.__host = host
        self.__init_urls()

    def __init_urls(self):
        baseurl = "{}://{}".format(self.__protocol, self.__host)
        self.get_video_play_url_callback = baseurl + "/API/GetPlayVideoUrlCallBack"
        self.get_video_play_url_list_by_videocode = baseurl + "/API/GetPlayVideoUrlListByVideoCode"
