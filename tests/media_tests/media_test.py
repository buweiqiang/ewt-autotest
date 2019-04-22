import json
import unittest

from common import helper
from conf import testdata
from media_site import media

media_web = media.Media()


class MediaTest(unittest.TestCase):
    @testdata.TestData
    def test_p1_get_video_play_url_with_callback_normally(self, dataobj):
        videocode = dataobj['videocode']
        result = media_web.get_video_play_url_callback("callback_123456", videocode)
        self.assertIn("callback_123456", result)
        json_str = helper.extract_string_in_bracket(result)
        json_data = json.loads(json_str)
        self.assertEqual(json_data['code'], 200, result)

    @testdata.TestData
    def test_p1_get_video_play_url_with_callback_incorrect_videocode(self, dataobj):
        videocode = dataobj['videocode']
        result = media_web.get_video_play_url_callback('incorrect_videocode', videocode)
        self.assertIn("incorrect_videocode", result)
        json_str = helper.extract_string_in_bracket(result)
        json_data = json.loads(json_str)
        self.assertEqual(json_data['code'], 200, result)
        self.assertEqual(json_data['data']['showPlat'], 0, result)

    @testdata.TestData
    def test_p1_get_video_play_url_by_videocode_normally(self, dataobj):
        videocode = dataobj['videocode']
        result = media_web.get_video_play_url_list_by_videocode(videocode)
        self.assertEqual(result['code'], 200, result)
        self.assertEqual(result['message'], "操作成功", result)
        self.assertGreater(len(result['data']['videolist']), 0, result)

    @testdata.TestData
    def test_p2_get_video_play_url_by_videocode_not_exist(self, dataobj):
        videocode = dataobj['videocode']
        result = media_web.get_video_play_url_list_by_videocode(videocode)
        self.assertEqual(result['code'], 130, result)
        self.assertEqual(result['message'], "该视频不存在!", result)
        self.assertEqual(len(result['data']['videolist']), 0, result)
