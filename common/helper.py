# coding=utf-8
import sys
import re
import string
import csv
import errno
import os
import random
import time
import hashlib
import shutil
import json
import base64

if sys.version > '3':
    PY3 = True
else:
    PY3 = False

_FILE_SLIM = (1 * 1024 * 1024)


def random_select_files(target_dir, count, loop_subfolders=False):
    if count < 1:
        raise ValueError('Invalid parameter "count", should > 0')
    file_names = []
    if loop_subfolders:
        for root, dirs, files in os.walk(target_dir):
            file_paths = [os.path.join(root, f) for f in files]
            file_names.extend(file_paths)
    else:
        file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                      os.path.isfile(os.path.join(target_dir, f))]

    random_files = random.sample(file_names, count)
    return random_files


def random_select_file(target_dir, count, loop_subfolders=False):
    file_names = []
    if loop_subfolders:
        for root, dirs, files in os.walk(target_dir):
            file_paths = [os.path.join(root, f) for f in files]
            file_names.extend(file_paths)
    else:
        file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                      os.path.isfile(os.path.join(target_dir, f))]
    filename = random.choice(file_names)
    return filename


def random_select_files_with_size_limit(target_dir, count, size_limit_mb=10):
    if count < 1:
        raise ValueError('Invalid parameter "count", should > 0')
    file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                  os.path.isfile(os.path.join(target_dir, f))]
    file_names = [f for f in file_names if os.path.getsize(f) < size_limit_mb * 1024 * 1024]
    random_files = random.sample(file_names, count)
    return random_files


def random_select_file_with_size_limit(target_dir, size_limit_mb=10):
    file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                  os.path.isfile(os.path.join(target_dir, f))]
    file_names = [f for f in file_names if os.path.getsize(f) < size_limit_mb * 1024 * 1024]
    random_file = random.choice(file_names)
    return random_file


def random_select_files_with_size_limit_min_max(target_dir, count=1, size_limit_max=20, size_limit_min=10):
    if count < 1:
        raise ValueError('Invalid parameter "count", should > 0')
    file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                  os.path.isfile(os.path.join(target_dir, f))]
    file_names = [
        f for f in file_names if size_limit_min * 1024 * 1024 < os.path.getsize(f) < size_limit_max * 1024 * 1024]
    random_files = random.sample(file_names, count)
    return random_files


def random_select_file_with_size_limit_min_max(target_dir, size_limit_max=20, size_limit_min=10):
    file_names = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if
                  os.path.isfile(os.path.join(target_dir, f))]
    file_names = [
        f for f in file_names if size_limit_min * 1024 * 1024 < os.path.getsize(f) < size_limit_max * 1024 * 1024]
    random_file = random.choice(file_names)
    return random_file


def list_compare(actual_list, expected_list):
    # 找出少的
    less = set(expected_list).difference(set(actual_list))
    # 找出多的
    more = set(actual_list).difference(set(expected_list))
    # 返回结果第一个是少了的，第二个是多了的
    return less, more


def get_random_string(length):
    ret = ''
    char = string.ascii_lowercase + string.digits + string.ascii_uppercase
    for i in range(length):
        ret += random.choice(char)
    return ret


def get_random_name(prefix="autotest"):
    name = '%s_%s_%s' % (prefix, get_random_string(3), int(time.time()))
    return name


def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def delete_dir(file_path):
    try:
        shutil.rmtree(file_path)
    except OSError:
        pass


# 获取字符串的md5加密
def get_str_md5(str):
    if type(str) is not bytes:
        str = str.encode('utf-8')
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


# 读取文件的md5值
def get_file_md5(filename):
    hashmethod = hashlib.md5()
    fp = open(filename, "rb")
    f_size = os.stat(filename).st_size

    while (f_size > _FILE_SLIM):
        hashmethod.update(fp.read(_FILE_SLIM))
        f_size -= _FILE_SLIM
    if f_size > 0:
        hashmethod.update(fp.read())

    return hashmethod.hexdigest()


def aes_encrypt_cbc(text, key, iv, block_size=16):
    '''
    这里密钥长度必须为16（AES-128）,24（AES-192）,或者32 （AES-256）Bytes 长度
    需要将传入的text,key,iv都转为bytes类型，否则在python3.6中会报错：TypeError: Object type <class 'str'> cannot be passed to C code
    :param text: 需加密的文本
    :param key: 密钥
    :param iv: 模式为CBC时，需指定偏移量
    :param block_size: 可以是8,16,32,64
    :return: 16进制字符串
    '''
    from Crypto.Cipher import AES
    key = key.encode()
    btext = pkcs7_pad(text, block_size).encode()
    iv = iv.encode()
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = cryptor.encrypt(btext)
    return encrypt_text


def aes_encrypt_ecb(text, key, block_size=16):
    '''
    aes encrypt with ecb mode
    :param text: text to encrypt
    :param key: key size should be times of 8
    :param block_size: block size
    :return:
    '''
    from Crypto.Cipher import AES
    key = key.encode()
    text = pkcs7_pad(text, block_size).encode()
    cryptor = AES.new(key, AES.MODE_ECB)
    encrypt_text = cryptor.encrypt(text)
    return encrypt_text


def des3_encrypt_cbc(text, key, iv=None, block_size=16):
    '''
    des加密只支持block_size=8，des3支持block_size为16，32，64
    :param text: 需加密的文本
    :param key: 密钥
    :param iv: 模式为CBC时，需指定偏移量
    :param block_size: des3支持block_size为16，32，64
    :return: base64 encode的字符串
    '''
    from Crypto.Cipher import DES3
    key = key.encode()
    btext = pkcs7_pad(text, block_size).encode()
    if iv:
        iv = iv.encode()
        cryptor = DES3.new(key, DES3.MODE_CBC, iv)
    else:
        cryptor = DES3.new(key, DES3.MODE_CBC)
    encrypt_text = cryptor.encrypt(btext)
    return encrypt_text


def des3_encrypt_ecb(text, key, block_size=16):
    '''
    des加密只支持block_size=8，des3支持block_size为16，32，64
    :param text: 需加密的文本
    :param key: 密钥
    :param block_size: des3支持block_size为16，32，64
    :return: base64 encode的字符串
    '''
    from Crypto.Cipher import DES3
    key = key.encode()
    btext = pkcs7_pad(text, block_size).encode()
    cryptor = DES3.new(key, DES3.MODE_ECB)
    encrypt_text = cryptor.encrypt(btext)
    return encrypt_text


def pkcs7_pad(text, length):
    count = len(text)
    pad_size = length - (count % length)
    text = text + (chr(pad_size) * pad_size)
    return text


# 读取文件的sha1值
def get_file_sha1(filename):
    hashmethod = hashlib.sha1()
    fp = open(filename, "rb")
    f_size = os.stat(filename).st_size

    while (f_size > _FILE_SLIM):
        hashmethod.update(fp.read(_FILE_SLIM))
        f_size -= _FILE_SLIM
    if f_size > 0:
        hashmethod.update(fp.read())

    return hashmethod.hexdigest()


def base64_encode_str(input):
    if isinstance(input, str):
        input = input.encode()
    encrypted_content = base64.b64encode(input)
    # 加密后的内容是bytes类型的，要解码为str类型返回
    return encrypted_content.decode()


def hex_str(input):
    # python3.5之前的python3版本，可以用如下方式转换为hex str
    # hex_text=''.join( [ "%02X" % x for x in text ] ).strip()
    # python3.6 可以直接用hex()函数
    if isinstance(input, str):
        input = input.encode()
    return input.hex()


def extract_string_in_bracket(text: str, opener='(', closer=')'):
    """
    获取括号中的字符串
    :param text: 要查找的字符串
    :param opener: 左括号，即开始符号
    :param closer: 右括号，即关闭符号
    :return: 查到的第一个字符串
    用正规表达式查找嵌套结构: 一不小心涉及了正则表达式一个很高级的功能，即平衡组/递归匹配，参考：
    https://blog.csdn.net/wrq147/article/details/6142285
    https://www.cnblogs.com/zs1111/archive/2009/11/12/1601951.html
    目前python还不支持平衡组的功能，所以只能自己实现了，参考：
    https://blog.csdn.net/maosijunzi/article/details/80092121

    none_oc_chars = "[^{0}{1}]*".format(opener, closer)
    p_str = r"\{0}" \
            r"{2}" \
            r"((" \
            r"(?'open'\{0})" \
            r"{2}" \
            r")+" \
            r"(" \
            r"(?'-open'\{1})" \
            r"{2}" \
            r")+)*" \
            r"(?(open)(?!))" \
            r"\{1}".format(opener, closer, none_oc_chars)
    """
    # 采用贪婪模式进行匹配，获取最外层括号里的内空
    p_str = r"\{0}(.*)\{1}".format(opener, closer)
    p = re.compile(p_str)
    result = re.search(p, text)
    if result:
        return result.group(1)
    return None


# 获取当前时间戳
def getCurrentTimeString(fmt='%Y-%m-%d %H:%M:%S'):
    datetime_str = time.strftime(fmt, time.localtime(time.time()))  # 把传入的元组按照格式，输出字符串
    # print '获取当前的时间：', Date
    return datetime_str


def check_identifier_type(user_identifier):
    identifier_type = None
    pattern_phone = re.compile('^([0+]\d{2,3})?-?\d{7,11}$')
    pattern_mail = re.compile('^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$')
    m_phone = pattern_phone.match(user_identifier)
    m_mail = pattern_mail.match(user_identifier)
    if m_phone:
        identifier_type = 'phone'
    elif m_mail:
        identifier_type = 'email'

    return identifier_type


def if_name_match(name_expect, name_actual, fuzzy_match):
    if fuzzy_match:
        return name_expect in name_actual
    else:
        return name_actual == name_expect


def read_pem_key_from_file(file_path):
    file_obj = open(file_path)
    print(file_obj)
    try:
        key = file_obj.read()
    finally:
        file_obj.close()
    return key


# 返回一个随机电话号码
def get_random_phone_number():
    list = ['139', '188', '185', '136', '155', '135', '158', '151', '152', '153']
    str = '0123456789'
    phone = random.choice(list) + ''.join(random.choice(str) for i in range(8))
    return phone


# 返回一个随机电话号码
def get_random_email():
    suffix = ['com', 'net', 'cn', 'org', 'de', 'fr', 'jp', 'in']
    domain = get_random_string(5)
    first_name = get_random_string(6)
    last_name = get_random_string(3)
    email = "{}_{}@{}.{}".format(first_name, last_name, domain, suffix)
    return email


def write_json_to_file(file_name, json_string):
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, file_name)
    file_write = open(file_path, 'a')
    sorted_json_string = json.dumps(json_string, sort_keys=True)
    file_write.write(sorted_json_string)
    file_write.write("\n")


# 写文件是建议都用wb的方式,防止windows操作系统做对换行符做转换
def write_bytes(file_path, content, append=False):
    write_mode = 'ab+' if append else 'wb'
    with open(file_path, write_mode) as to_file:
        print('write content type:', type(content))
        # 在python3中,str和unicode都统一为str了,wb的话需要将string编码为bytes再写入
        # 在python2中str和bytes是同一类型,当content是unicode时,需要将unicode编码为str(bytes)
        if not isinstance(content, bytes):
            content = content.encode('utf-8')
        to_file.write(content)


# 注意中文版windows的默认写入的编码格式是gbk
def write_file(file_path, str_content, append=False):
    write_mode = 'a+' if append else 'w'
    with open(file_path, write_mode) as to_file:
        print('write content type:', type(str_content))
        # 无论python2和3,只要content是str就行
        # python2需要将unicode编码为str,python3需将bytes类型解码为str
        to_file.write(str_content)


# 注意中文版windows的默认写入的编码格式是gbk
def write_csv(file_path, row, append=False):
    write_mode = 'a+' if append else 'w'
    with open(file_path, write_mode) as to_file:
        writer = csv.writer(to_file)
        writer.writerow(row)


def read_file(file_path):
    with open(file_path, 'r') as f:
        while True:
            l = f.readline()
            if not l:
                break
            print('read type:{}, content:{}'.format(type(l), l))


# 如果文件是text类型的话,建议还是用r吧,会自动解码
def read_bytes(file_path):
    # 在python2中,rb的读出的内容编码为str类型
    # 在python3中,rb的读出的内容编码为bytes类型,需要自己解码
    with open(file_path, 'rb') as f:
        while True:
            l = f.readline()
            if not l:
                break
            print('read type:{}, content:{}'.format(type(l), l))


def read_csv_last_line(file_path, ignore_empty_line=True):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        last_line = []
        for line in reader:
            if ignore_empty_line:
                if line:
                    last_line = line
            else:
                last_line = line
    # print('csv last line type:', type(last_line))
    return last_line


def read_file_last_line(file_path, ignore_empty_line=True):
    # 中文windows下的sys.getdefaultencoding是utf-8,但是写入时默认gbk
    # print ('sys encoding:', sys.getdefaultencoding())
    last_line = ''
    with open(file_path, 'r') as f:
        while True:
            l = f.readline()
            # print ('--length: {}, content: {}'.format(len(l), l))
            if not l:
                break
            elif ignore_empty_line:
                last_line = l if l.strip() else last_line
            else:
                last_line = l
    # print('last line type is:', type(last_line))
    return last_line


# 通过rb的方式读出来的内容是bytes类型的,在解码时要根据写入时的类型来解码,解码格式不对会报错
# 注意中文版windows的默认编码格式是gbk
def read_file_last_line_bytes(file_path):
    last_line = ''
    with open(file_path, 'rb') as f:
        f.seek(0, 2)
        f_length = f.tell()
        count_line_found = 0
        if f_length > 0:
            # 如果文件长度大于0,从文件末尾开始向前移动2位(读取1个字符会导致指针后移1位)
            for i in range(f_length):
                f.seek(-i - 1, 2)
                c = f.read(1)
                if c == '\n':
                    count_line_found += 1
                # 至少要找到两个换行才break
                if count_line_found > 1:
                    break
            # 因为最后有一个读的操作导致指针向前移动了1位,所以最后要反向移一位
            f.seek(-1, 1)
            lines = f.readlines()
            last_line = lines[-1]  # 取最后一行
    # print('last line type is:', type(last_line))
    # 在python2中,rb的读出的内容编码为str类型,无需解码
    # 在python3中,rb的读出的内容编码为bytes类型,需要自己根据写入的编码类型解码
    return last_line
