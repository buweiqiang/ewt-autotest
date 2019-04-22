import os
import functools
import glob
from conf.config import ENV


class TestDataType:
    ini = 'ini'
    json = 'json'
    xml = 'xml'


class dataobject:
    # 数据模板：{"testclass": {"xxx_class": {"testcase": {"xxx_case": {"key": "value", "key2": "value2"}}}}}
    def __init__(self, file_name, data_type=TestDataType.ini):
        if not file_name:
            raise ValueError("file_name can't be null or empty")
        if not os.path.exists(file_name):
            raise IOError("file {} not exists".format(file_name))
        self.filename = file_name
        self.data_type = data_type
        self.data = {}

    def loadtestdata(self):
        # load test data from file, based on data_type
        loader_switcher = {
            'ini': load_test_data_from_ini,
            'json': load_test_data_from_json,
            'xml': load_test_data_from_xml
        }

        load_func = loader_switcher.get(self.data_type)
        if load_func:
            self.data = load_func(self.filename)
        else:
            raise NotImplementedError("loader for {} is not implemented".format(self.data_type))

    def gettestcasedata(self, class_name, case_name):
        if self.data and 'testclass' in self.data:
            cls_data = self.data['testclass'].get(class_name)
            if cls_data and 'testcase' in cls_data:
                return cls_data['testcase'].get(case_name, {})
        return {}


def load_test_data_from_ini(file_name):
    import configparser
    data = {"testclass": {}}
    config = configparser.RawConfigParser()
    config.read(file_name)
    for s in config.sections():
        _cls, _tc = s.split('.')
        if not _cls in data["testclass"]:
            data["testclass"][_cls] = {"testcase": {}}
        data["testclass"][_cls]["testcase"][_tc] = dict(config.items(s))
    return data


def load_test_data_from_json(file_name):
    import json
    with open(file_name) as json_file:
        json_data = json.load(json_file)
        return json_data


def load_test_data_from_xml(file_name):
    import xml.etree.ElementTree as ET
    xml_dict = {"testclass": {}}
    xtree = ET.parse(file_name)
    root = xtree.getroot()
    for cls_node in root.findall('testclass'):
        cls_name = cls_node.attrib['name']
        xml_dict["testclass"][cls_name] = {"testcase": {}}
        for tc_node in cls_node:
            tc_name = tc_node.attrib['name']
            xml_dict["testclass"][cls_name]["testcase"][tc_name] = {}
            for kv in tc_node:
                xml_dict["testclass"][cls_name]["testcase"][tc_name][kv.tag] = kv.text

    return xml_dict


def discover_test_data_file(py_file_name, env):
    file_name = ''
    # 通过splitext拿到去除后缀的数据文件名
    _name, _ext = os.path.splitext(py_file_name)
    # 数据文件类型默认是ini
    data_type = TestDataType.ini
    # 找到所有符合条件的数据文件
    if env:
        # 优先使用符合环境参数的数据文件
        path_format = "{}.{}.*".format(_name, env)
        find_result = glob.glob(path_format)
        if find_result and len(find_result) > 0:
            file_name = os.path.abspath(find_result[0])

    # 如果未找到相应的数据文件，使用默认规则查找数据文件
    if not file_name:
        path_format = "{}.*".format(_name)
        find_result = glob.glob(path_format)
        for f in find_result:
            # 认定第一个非py结尾的文件就是数据文件
            if not f.endswith(".py"):
                file_name = os.path.abspath(f)
                break

    # 如果仍未找到相应的数据文件，抛出异常
    if not file_name:
        raise FileNotFoundError("data file for {} not found".format(py_file_name))

    # 根据文件后缀最终确定文件的类型
    f_name, f_ext = os.path.splitext(file_name)
    if "json" in f_ext:
        data_type = TestDataType.json
    if "xml" in f_ext:
        data_type = TestDataType.xml

    return file_name, data_type


def TestData(testmethod):
    """
    decorator of test method
    :param testmethod: the original method which has been decorated
    :return: a test method with a test data object
    """

    @functools.wraps(testmethod)
    def __loadtestdata(*args, **kwargs):
        tc_data = {}
        if len(args) > 0:
            # print('data2: {}'.format(args[0].__class__.__dict__))
            # print('data test name: {}'.format(args[0]._testMethodName))
            # print("data module name: {}".format(args[0].__module__))
            # module_name = testmethod.__module__
            func_code = testmethod.__code__
            class_name = args[0].__class__.__name__
            case_name = testmethod.__name__

            # find the data file which has the same name with module name
            data_file, data_type = discover_test_data_file(func_code.co_filename, ENV)
            # load test data from the data_file
            if data_file:
                data = dataobject(data_file, data_type)
                data.loadtestdata()
                # get key/value list for test case, append to args
                tc_data = data.gettestcasedata(class_name, case_name)
        args += (tc_data,)
        return testmethod(*args, **kwargs)

    return __loadtestdata


if __name__ == '__main__':
    f, t = discover_test_data_file(r'..\tests\media_tests\media_test.py', 'test')
    print(f, t)
