# 这个文件专门用来存储e网通相关常量
WEB_AES_IV = "2017110912453698"
WEB_AES_KEY = "20171109124536982017110912453698"
APP_AES_KEY = "eo^nye1j#!wt2%v)"

# 移动端登陆时需要用到的sgin值
ios_sign = '7ios5f576beec73f652a045904ef15101'
android_sign = '6faa3e603feba8003ca858ceb694bc81a'
web_sign = '2www465b1dbd68d0578f7fa2a28049523'
# 移动端接口用来计算userid的值
userid_keybin = 30205014

# 修改用户头像的可选头像列表
user_photo_src_list = ["/Content/images/photos/p{0}.jpg".format(i + 1) for i in range(20)]
expect_km_names = ['数学', '生物', '英语', '语文', '物理', '化学', '历史', '地理', '政治', '其他', '通用技术', '美术', '至尊专区']

class RequestSignMode():
    no_token_no_sort_value_list = 1
    no_token_no_sort_key_value_list = 2
    no_token_sort_value_list = 3
    no_token_sort_key_value_list = 4
    token_no_sort_value_list = 11
    token_no_sort_key_value_list = 12
    token_sort_value_list = 13
    token_sort_key_value_list = 14

    @staticmethod
    def all_sign_modes():
        all_modes = []
        for k, v in RequestSignMode.__dict__.items():
            if not k.startswith("__") and type(v) is int:
                all_modes.append(v)
        return all_modes
