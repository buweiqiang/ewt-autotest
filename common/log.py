import logging
import time

import os


class LogType():
    EWT_APP = "EWT_APP"
    EWT_WEB = "EWT_WEB"
    OA_WEB = "OA_WEB"
    OA_APP = "OA_APP"
    EWT_COMMON = "EWT_COMMON"


def initLogger(name=__file__, level='INFO', logfile=None):
    logging.basicConfig(level=level, format='%(name)-10s: %(levelname)+8s: %(message)s')

    logger = logging.getLogger(name)
    if logfile is not None:
        fh = logging.FileHandler(logfile)
        fh.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s @%(filename)s[%(lineno)d]')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


def getLoggerForEWT(logtype=LogType.EWT_WEB):
    from conf import config
    ewt_config = config.getEWTConfig()
    loglevel = ewt_config.getLogLevel()
    logfile = None
    if ewt_config.getLogToFile().lower() == 'true':
        filename = logtype + '_' + time.strftime('%Y-%m-%d.log')
        logdir = ewt_config.getLogDir()
        logfile = os.path.join(logdir, filename)
    return initLogger(logtype, loglevel, logfile)


if __name__ == '__main__':
    logging.info('info from root')
    logging.warning('warning from root')
    logger = initLogger(level=23)
    # logger = initLogger('test',logfile='/Users/boweiqiang/autotest.log')
    logger.info('info by logger')
    logger.warning('warning by logger')
    logger = getLoggerForEWT()
    logger.warning('test by ewt')
