from common import log
from conf import config
from ewt.ewt_client import EWTClient
from ewt.study_lib.study_urls import StudyUrls

logger = log.getLoggerForEWT()
ewt_cfg = config.getEWTConfig()
protocol = ewt_cfg.getProtocol()
study_host = ewt_cfg.getStudyHost()


class Study(object):
    """
    构造函数中的ewt_client即可以是ewt_web_client，也可以是ewt_app_client，做到同一个接口兼容app/pc端发送的请求
    请求如何发送，由实例化时传入的ewt_client决定，study只用关心接口的参数逻辑，而不用关心请求发送的逻辑
    """

    def __init__(self, ewt_client: EWTClient):
        self.client = ewt_client
        self.url_builder = StudyUrls(protocol, study_host)

    def get_recommend_course(self):
        ret_json = self.client.get(self.url_builder.kecheng_get_recommend_course)
        return ret_json

    def get_index_banner_info(self):
        ret_json = self.client.get(self.url_builder.kecheng_get_index_banner_info)
        return ret_json

    def get_homepage_course_list(self):
        ret_json = self.client.get(self.url_builder.kecheng_get_homepage_course_list)
        return ret_json

    def get_lesson_comment_list(self, lensson_id, page=1, type=1, index=0):
        # LessonId=1403&page=1&type=1&index=0
        post_data = {"LessonId": lensson_id, "page": page, "type": type, "index": index}
        ret_json = self.client.post(self.url_builder.kecheng_get_comment_list, data=post_data)
        return ret_json

    def get_course_detail(self, courseid):
        post_data = {"courseid": courseid}
        ret_json = self.client.post(self.url_builder.courseservice_get_course_detail, data=post_data)
        return ret_json

    def get_lesson_detail(self, lessonid):
        post_data = {"lessonid": lessonid}
        ret_json = self.client.post(self.url_builder.courseservice_get_lesson_detail, data=post_data)
        return ret_json

    def get_kemulist(self):
        ret_json = self.client.post(self.url_builder.appstudyapi_get_kemulist)
        return ret_json

    def get_knowledge_course(self, km, k=0, group=0, type=0, sort=1, page=1, hl=0, s=0, t=''):
        params = {"k": k, "g": group, "hl": hl, "t": t, "s": s, "sort": sort, "page": page, "km": km, "type": type}
        ret_json = self.client.get(self.url_builder.appstudyapi_get_knowledge_course, params=params)
        return ret_json
