import argparse
import os
import datetime
import fnmatch

REPORT_FOLDER = 'TestResult'
LOG_FOLDER = 'TestLog'
try:
    from conf import config

    g_cfg = config.getGlobalConfig()
    log_dir = g_cfg.getLogDir()
    LOG_FOLDER = os.path.basename(os.path.realpath(log_dir))
except:
    pass


def delete_files(file_name_pattern="*.log", start_dir=os.getcwd(), before_days=30):
    print('Start to delete {} files {} days ago under {}'.format(file_name_pattern, before_days, start_dir))
    found_count = 0
    expired_count = 0
    deleted_count = 0
    if not start_dir:
        start_dir = os.getcwd()
    for root, dirs, files in os.walk(start_dir):
        for f in files:
            f_path = os.path.join(root, f)
            if fnmatch.fnmatch(f, file_name_pattern):
                found_count += 1
                create_time = datetime.datetime.fromtimestamp(os.path.getctime(f_path))
                n_days_ago = (datetime.datetime.now() - datetime.timedelta(days=int(before_days)))
                if create_time < n_days_ago:
                    expired_count += 1
                    try:
                        print('deleting file: {}'.format(f_path))
                        os.remove(f_path)
                        deleted_count += 1
                    except Exception as e:
                        print(e)
    print('Cleanup result under {0}: Found: {1}, expired: {2}, deleted: {3}'.format(start_dir, found_count,
                                                                                    expired_count, deleted_count))


class ResultCleaner(object):
    def __init__(self, report_forlder=REPORT_FOLDER):
        self.report_folder = report_forlder

    def delete_reports(self, before_days=30):
        return delete_files("*.html", self.report_folder, before_days)


class LogCleaner(object):
    def __init__(self, log_folder=LOG_FOLDER):
        self.log_folder = log_folder

    def delete_logs(self, before_days=30):
        return delete_files("*.log", self.log_folder, before_days)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fnpattern', help='the pattern of file name to delete, e.g., *.log')
    parser.add_argument('-s', dest='start_dir', help='the start dir to search test results')
    parser.add_argument('-d', dest='days', default=30, help='delete report N days ago')
    args = parser.parse_args()

    # delete report files N days ago, N >=7
    if int(args.days) < 7:
        print('days must equal or greater than 7')
    else:
        delete_files(args.fnpattern, args.start_dir, args.days)
