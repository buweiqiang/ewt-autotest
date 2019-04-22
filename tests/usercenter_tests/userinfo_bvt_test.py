import unittest
from ewt import ewt_web, ewt_const
from  conf import config
import random

ewt_cfg = config.getEWTConfig()
student_name = ewt_cfg.getStudentUser()
student_password = ewt_cfg.getStudentPassword()
student1 = ewt_web.EWTWeb(student_name, student_password)


class UserInfoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("# This is class setup")
        verify_expire_result = student1.usercenter.verify_is_expired_member()
        print(verify_expire_result)

    @classmethod
    def tearDownClass(cls):
        print("# This is class teardown")
        student1.www.edit_user_photo(ewt_const.user_photo_src_list[0])

    def test_p1_edit_user_photo_normally(self):
        photo_src = random.choice(ewt_const.user_photo_src_list)
        edit_result = student1.www.edit_user_photo(photo_src)
        self.assertTrue(edit_result['Result'], edit_result['Msg'])

    def test_p3_edit_user_photo_incorrect_src(self):
        photo_src = "/Content/images/photos/p21"
        edit_result = student1.www.edit_user_photo(photo_src)
        self.assertFalse(edit_result['Result'], edit_result['Msg'])
