import unittest

from  conf import config, testdata
from ewt import ewt_web

ewt_cfg = config.getEWTConfig()
student_name = ewt_cfg.getStudentUser()
student_password = ewt_cfg.getStudentPassword()
student_web = ewt_web.EWTWeb(student_name, student_password)


class KechengTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("# This is class setup")

    @classmethod
    def tearDownClass(cls):
        print("# This is class teardown")

    @testdata.TestData
    def test_p1_kecheng_get_lesson_comment_list(self, dataobj):
        lessonid = dataobj['lessonid']
        get_comment_result = student_web.study.get_lesson_comment_list(lessonid)
        self.assertIn("lessoninfo", get_comment_result, get_comment_result)
        comment_count = get_comment_result['count']
        print("Comment count of lesson {}: {}".format(lessonid, get_comment_result['count']))
        data_count = len(get_comment_result['data'])
        for i in range(1, 100):
            key = "data{}".format(i)
            if key in get_comment_result:
                data_count += len(get_comment_result[key])
            else:
                break
        self.assertEqual(data_count, comment_count,
                         "actual data count is {}, not equal to comment count {}".format(data_count, comment_count))
