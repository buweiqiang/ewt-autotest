import unittest
import random
from ewt import ewt_app
from  conf import config
from ewt.ewt_const import expect_km_names

ewt_cfg = config.getEWTConfig()
student_name = ewt_cfg.getStudentUser()
student_password = ewt_cfg.getStudentPassword()
student_app = ewt_app.EWTApp(student_name, student_password)
student_app.set_os_version('593')


class CourseServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("# This is class setup")

    @classmethod
    def tearDownClass(cls):
        print("# This is class teardown")

    def test_p1_get_km_list(self):
        # step 1, 获取科目列表
        km_result = student_app.study.get_kemulist()

        # 检查科目的数量，并打印排序后的列表
        km_names = [k['Name'] for k in km_result['data']]
        print("find km count: {}".format(len(km_names)))
        print("origin km names: {}".format(km_names))
        km_names.sort()
        print("sorted km names: {}".format(km_names))

        # 判断期望的科目列表是返回列表的子集
        self.assertLess(set(expect_km_names), set(km_names))

    def test_p1_courseservice_get_lesson_detail(self):
        # step 1, 获取科目列表，并随机选取一个科目
        km_result = student_app.study.get_kemulist()
        # 必须从期望的列表中选择，因为获取科目列表接口返回的科目有多余的，这个可以算作是科目列表接口的bug
        km = random.choice([k for k in km_result['data'] if k['Name'] in expect_km_names])
        print("random select a km: {}(km={})".format(km['Name'], km['ID']))

        # step 2, 跟据科目获取课程列表，并随机选择一个课程
        course_result = student_app.study.get_knowledge_course(km['ID'])
        # print(course_result)
        course_list = [c for c in course_result['data']['list']]
        course = random.choice(course_list)
        print("random select a course: {}(id={})".format(course['title'], course['id']))

        # step 3, 跟据课程获取讲列表，并随机选择一个讲
        course_detail = student_app.study.get_course_detail(course['id'])
        for lesson in course_detail['data']['lessonlist']:
            print("{}: {}".format(lesson['lessonid'], lesson['lessontitle']))
            print("-- videolist count: {}".format(len(lesson['videolist'])))
        lesson = random.choice(course_detail['data']['lessonlist'])
        print("random select a lesson: {}(id={})".format(lesson['lessontitle'], lesson['lessonid']))

        # step 4, 调用获取讲详情的接口，并检查返回结果
        lesson_detail = student_app.study.get_lesson_detail(lesson['lessonid'])
        self.assertIn('data', lesson_detail, lesson_detail)
        for lesson in lesson_detail['data']['lessonlist']:
            self.assertIn('lessonid', lesson, "lesson id not found")
            self.assertIn('lessontitle', lesson, "lesson title not found")
            print("{}: {}".format(lesson['lessonid'], lesson['lessontitle']))
            print("-- videolist count: {}".format(len(lesson['videolist'])))
