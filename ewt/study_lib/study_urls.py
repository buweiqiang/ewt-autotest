class StudyUrls(object):
    def __init__(self, protocol, host):
        self.__protocol = protocol
        self.__host = host
        self.__init_urls()

    def __init_urls(self):
        baseurl = "{}://{}".format(self.__protocol, self.__host)
        self.kecheng_get_index_banner_info = baseurl + "/kecheng/GetIndexBannerInfo"
        self.kecheng_get_recommend_course = baseurl + "/kecheng/GetRecmdCourse"
        self.kecheng_get_homepage_course_list = baseurl + "/kecheng/GetStudyHomePageCourseList"
        self.kecheng_get_comment_list = baseurl + "/kecheng/GetCommentList"
        self.appstudyapi_get_kemulist = baseurl + "/AppStudyApi/GetFollowKemuListByUserId"
        self.appstudyapi_save_kemulist = baseurl + "/AppStudyApi/SaveFollowKemuByUserId"
        self.appstudyapi_get_home_page_data = baseurl + "/AppStudyApi/GetHomePageData"
        self.appstudyapi_get_knowledge_course = baseurl + "/AppStudyApi/KnowledgeCourse"
        self.appstudyapi_get_course_info = baseurl + "/AppStudyApi/CourseInfos"
        self.appstudyapi_get_course_detail2 = baseurl + "/AppStudyApi/CourseDetails2"
        self.courseservice_get_course_detail = baseurl + "/CourseService/getcoursedetail"
        self.courseservice_get_lesson_detail = baseurl + "/CourseService/getlessondetail"
