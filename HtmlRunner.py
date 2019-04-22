import argparse
import os
import time
import unittest

import HTMLTestRunner
from conf import config

REPORT_FOLDER = 'TestResult'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('start_dir', help='start dir to discover tests')
    parser.add_argument('-p', dest='pattern', default='*_test.py', help='pattern of python test files')
    parser.add_argument('-m', dest='method_prefix', default='test', help='method prefix to match test cases')
    parser.add_argument('-o', dest='output', help='specify the output html')
    parser.add_argument('-d', dest='days', default=30, help='delete report N days ago')
    parser.add_argument('-e', dest='env', help='test environment to run tests')
    args = parser.parse_args()

    # delete report files N days ago
    if int(args.days) < 7:
        args.days = 7

    try:
        # try cleanup test reports and test log
        # what ever delete succeed or not, pass to run test cases
        from cleanup import ResultCleaner, LogCleaner

        result_cleaner = ResultCleaner(REPORT_FOLDER)
        result_cleaner.delete_reports(before_days=args.days)
        log_cleaner = LogCleaner()
        log_cleaner.delete_logs(before_days=args.days)
    except:
        pass
    # finally:
    #     pass

    # set env
    config.ENV = args.env

    # load tests
    loader = unittest.defaultTestLoader
    loader.testMethodPrefix = args.method_prefix
    suite = unittest.defaultTestLoader.discover(start_dir=args.start_dir, pattern=args.pattern)
    print('test discover pattern is: \"%s\", case count: %s' % (args.pattern, suite.countTestCases()))

    # define output report file
    if not os.path.exists(REPORT_FOLDER):
        os.mkdir(REPORT_FOLDER)
    if args.output:
        output = args.output
    else:
        output = 'auto_test_report_' + time.strftime('%Y-%m-%d_%H-%M-%S.html')
    if not output.endswith('.html'):
        output = output + '.html'
    report_file = os.path.join(REPORT_FOLDER, output)

    # run tests and generate report
    print('Test report will be generated at: %s' % report_file)
    with open(report_file, 'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(fp, title='auto test report')
        result = runner.run(suite)
        print('Test report generated at: %s' % report_file)
        result_summary = 'Total: %s, succeed: %s, failure: %s, error: %s' % (suite.countTestCases(),
                                                                             result.success_count, result.failure_count,
                                                                             result.error_count)
        print(result_summary)
        if result.failure_count > 0 or result.error_count > 0:
            raise AssertionError(result_summary)
