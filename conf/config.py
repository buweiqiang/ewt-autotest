# coding=utf-8
import argparse
import os
import sys
import types
import shutil

if sys.version > '3':
    PY3 = True
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')
    PY3 = False

CONF_DIR = os.path.dirname(__file__)

if not PY3:
    import ConfigParser as configparser
else:
    import configparser


class ConfigType():
    EWT = 'ewt'
    OA = 'oa'
    MEDIA = 'media'

    @staticmethod
    def config_types():
        all_types = []
        for k, v in ConfigType.__dict__.items():
            if not k.startswith("__") and type(v) is str:
                all_types.append(v)
        return all_types


def getConfigFiles(config_type, env):
    if config_type not in ConfigType.config_types():
        raise ValueError("config type not defined: {}".format(config_type))

    configfiles = []
    # 加载全局配置文件,一定存在
    _global_file = os.path.join(CONF_DIR, 'global.cfg')
    configfiles.append(_global_file)

    # 加载指定产品组(config_type)的全局配置文件, 可能不存在
    _product_global_file = os.path.join(CONF_DIR, '{}.global.cfg'.format(config_type))
    if os.path.exists(_product_global_file):
        configfiles.append(_product_global_file)

    # 加载指定env的配置文件config_type.env.cfg,如不存在,默认为config_type.cfg
    _config_file = None
    if env:
        _config_file = os.path.join(CONF_DIR, '{}.{}.cfg'.format(config_type, env))
        if not os.path.exists(_config_file):
            print('%s not found, will use the default one' % _config_file)
            _config_file = None
    if not _config_file:
        _config_file = os.path.join(CONF_DIR, '{}.cfg'.format(config_type))
    configfiles.append(_config_file)

    return configfiles


# 通过实现__new__方法实现单例模式
# 将一个类的实例绑定到类变量_instance上,
# 如果cls._instance为None说明该类还没有实例化过,实例化该类,并返回
# 如果cls._instance不为None,直接返回cls._instance
class Singleton(object):
    instance = None

    def __new__(cls, *args, **kw):
        # if not hasattr(cls, '__instance'):
        if not cls.instance:
            orig = super(Singleton, cls)
            cls.instance = orig.__new__(cls)
        return cls.instance


class Config(object):
    def __init__(self, config_files):
        if isinstance(config_files, str):
            config_files = [config_files]
        __config_files = []
        for conf_file in config_files:
            if not os.path.exists(conf_file):
                conf_file = os.path.join(CONF_DIR, conf_file)
            __config_files.append(conf_file)
        self.config = configparser.RawConfigParser()
        self.config.read(__config_files)

    def getItemValue(self, section, itemkey):
        return self.config.get(section, itemkey)

    def setItemValue(self, section, item_key, item_value):
        self.config.set(section, item_key, item_value)

    def getLogLevel(self):
        level = self.config.get('log', 'log_level')
        return level.upper()

    def getLogToFile(self):
        return self.config.get('log', 'log_to_file')

    def getLogDir(self):
        log_dir = self.config.get('log', 'log_dir')
        return os.path.join(CONF_DIR, log_dir)

    def getTestDataDir(self):
        data_dir = self.config.get('test', 'testdatadir')
        return os.path.join(CONF_DIR, data_dir)

    def getPCUserAgent(self):
        if not self.config.has_option('test', 'pc_user_agent'):
            return 'AutoTest/5.0'
        return self.config.get('test', 'pc_user_agent')

    def getMobileUserAgent(self):
        if not self.config.has_option('test', 'mobile_user_agent'):
            return 'Android 6.0'
        return self.config.get('test', 'mobile_user_agent')


class GlobalConfig(Singleton, Config):
    def __init__(self):
        self.config_file = os.path.join(CONF_DIR, 'global.cfg')
        if not hasattr(self, 'config'):
            Config.__init__(self, self.config_file)

    def getENV(self):
        if not self.config.has_option('test', 'env'):
            return None
        env = self.config.get('test', 'env')
        if env.lower() in ("none", "default"):
            env = None
        return env


class EWTConfig(Singleton, Config):
    def __init__(self):
        # 因为多继承的原因，每次new不产生新实例，但是会多次初始化，这里要避免多次初始化
        if not hasattr(self, 'config'):
            config_files = getConfigFiles(ConfigType.EWT, ENV)
            Config.__init__(self, config_files)

    def getProtocol(self):
        if not self.config.has_option('ewt', 'protocol'):
            return 'http'
        return self.config.get('ewt', 'protocol')

    def getWWWHost(self):
        return self.config.get('www', 'host')

    def getUserCenterHost(self):
        return self.config.get('usercenter', 'host')

    def getStudyHost(self):
        return self.config.get('study', 'host')

    def getTeacherHost(self):
        return self.config.get('teacher', 'host')

    def getStudentUser(self):
        return self.config.get('ewt', 'student_user')

    def getStudentPassword(self):
        return self.config.get('ewt', 'student_password')

    def getTeacherUser(self):
        return self.config.get('ewt', 'teacher_user')

    def getTeacherPassword(self):
        return self.config.get('ewt', 'teacher_password')

    def getNetSchoolUser(self):
        return self.config.get('netschool', 'user')

    def getNetSchoolPassword(self):
        return self.config.get('netschool', 'password')


class OAConfig(Singleton, Config):
    def __init__(self):
        if not hasattr(self, 'config'):
            config_files = getConfigFiles(ConfigType.OA, ENV)
            Config.__init__(self, config_files)


class MediaConfig(Singleton, Config):
    def __init__(self):
        # 因为多继承的原因，每次new不产生新实例，但是会多次初始化，这里要避免多次初始化
        if not hasattr(self, 'config'):
            config_files = getConfigFiles(ConfigType.MEDIA, ENV)
            Config.__init__(self, config_files)

    def getProtocol(self):
        if not self.config.has_option('media', 'protocol'):
            return 'http'
        return self.config.get('media', 'protocol')

    def getHost(self):
        return self.config.get('media', 'host')

    def getUser(self):
        return self.config.get('media', 'user')

    def getPassword(self):
        return self.config.get('media', 'password')


def getGlobalConfig():
    return GlobalConfig()


def getEWTConfig():
    return EWTConfig()


def getMediaConfig():
    return MediaConfig()


def getOAConfig():
    return OAConfig()


def getConfig(config_type):
    conf_type_switcher = {
        ConfigType.EWT: EWTConfig,
        ConfigType.OA: OAConfig,
        ConfigType.MEDIA: MediaConfig
    }

    cfg_class = conf_type_switcher.get(config_type)
    if not cfg_class:
        raise ValueError('Appropriate class not found for config type: %s' % config_type)
    return cfg_class()


# global.cfg是必须存在的，里面test.env是基础配置
global_cfg = GlobalConfig()
ENV = global_cfg.getENV()

if __name__ == '__main__':
    '根据环境加载配置文件'
    parser = argparse.ArgumentParser()
    parser.add_argument('env', nargs='?', help='specify the environment to be set to')
    parser.add_argument('-l', dest='log_level', default='', help='log level: debug/info/warn/error/fatal')

    args = parser.parse_args()
    if args.env:
        print('Setting env to ', args.env)
        global_cfg.setItemValue('test', 'env', args.env)
        with open(global_cfg.config_file, 'w') as fp:
            global_cfg.config.write(fp)
            print('- set env to {} in {}'.format(args.env, global_cfg.config_file))
            fp.close()
        # 将所有的配置文件*.cfg的内容替换为*.env.cfg的内容
        for t in ConfigType.config_types():
            _orig_file = os.path.join(CONF_DIR, '%s.cfg' % t)
            _bak_file = '%s.bak' % _orig_file
            _tobe_file = os.path.join(CONF_DIR, '%s.%s.cfg' % (t, args.env))
            config = configparser.ConfigParser()

            # config.read(_orig_file) # 不读原始文件，因为会读入一些上次修改遗留的不必要参数
            if os.path.exists(_tobe_file):
                # backup original config file
                if not os.path.exists(_bak_file):
                    print('backed up %s to %s' % (_orig_file, _bak_file))
                    os.rename(_orig_file, _bak_file)
                # 用写文件代替拷贝，好处是可以做到合并，原配置文件中公用的变量不会丢掉
                config.read(_tobe_file)  # 直接read tobe file，相当于拷贝替换
                # 换回使用拷贝替换，合并会带入一些不需要的参数
                # shutil.copyfile(_tobe_file, _orig_file)
                print('- loaded: %s' % _tobe_file)
            else:
                print('* not found: %s' % _tobe_file)
                continue

            # 配置日志级别，方便调试时打印更多的信息
            if args.log_level:
                if not config.has_section('log'):
                    config.add_section('log')
                config.set('log', 'log_level', args.log_level)

            # 将加载的特定环境的配置写回默认配置文件
            with open(_orig_file, 'w') as fp:
                config.write(fp)
                fp.close()
    else:
        print('supported config types:')
        for t in ConfigType.config_types():
            print(t)
