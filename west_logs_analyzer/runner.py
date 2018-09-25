import argparse
import tempfile

from datasketch.minhash import MinHash
from datasketch.lsh import MinHashLSH

from west_logs_analyzer import __version__
from west_logs_analyzer.chart_builder import StackedBarChartBuilder
from west_logs_analyzer.import_logs import FakeRetriever, SqlLogsRetriever
from west_logs_analyzer.reporter import ErrorEmailNotificator
from west_logs_analyzer.utils import get_days_range, print_now

NUM_PERM = 256

class Runner(object):
    def __init__(self, dbUser, dbPwd, interval):
        self.retriever = SqlLogsRetriever(dbUser, dbPwd)
        self.days_range = get_days_range(interval)
        self.data = []

    def analyze_logs(self):
        self._collect_log_data()

        (min_hashes, lsh) = self._create_min_hashes()
        
        groups = self._group_logs(min_hashes, lsh)

        results = self._prepare_results(groups)

        temp_file = open('chart.png', 'w')
        chart = StackedBarChartBuilder(self.days_range, results)
        chart.build_chart(temp_file.name)
        temp_file.close()

        print_now('Just about to send notification')
        notificator = ErrorEmailNotificator(self.days_range, results, temp_file.name)
        notificator.send_notification()
        print_now('Done')

    def _prepare_results(self, groups):
        results = []

        for idx, key in enumerate(groups):
            text = groups[key]['text']

            errors = []
            for day in self.days_range:
                count = self._get_log_counts(day, groups[key]['items'])
                errors.append((day, count))

            results.append((idx, text, errors))

        return results

    def _intersection(self, lst1, lst2):
        return list(set(lst1) & set(lst2))

    def _get_log_counts(self, day, group_items):
        items = [event_id for (event_id, timestamp, _) in self.data if 
            timestamp.year == day.year and timestamp.month == day.month and timestamp.day == day.day]
        counts = len(self._intersection(group_items, items))
        return counts

    def _collect_log_data(self):
        for day in self.days_range:
            print_now('Start to query logs for {}'.format(day.strftime('%m/%d/%Y')))
            logs = self.retriever.get_logs(day)
            print_now('{} logs found for {}'.format(len(logs), day.strftime('%m/%d/%Y')))
            for log in logs:
                self.data.append(log)

    def _create_min_hashes(self):
        print_now('Start creating min hashes')
        min_hashes = []
        for (event_id, _, stacktrace) in self.data:
            if stacktrace is None: continue

            l_set = set(stacktrace.lower().replace(',', ' ').split())
            m = MinHash(num_perm=NUM_PERM)
            for d in l_set:
                m.update(d.encode('utf8'))
            min_hashes.append((event_id, m))

        lsh = MinHashLSH(threshold=0.5, num_perm=NUM_PERM)
        for event_id, m in min_hashes:
            lsh.insert(event_id, m)

        return (min_hashes, lsh)

    def _group_logs(self, min_hashes, lsh):
        print_now('Start grouping logs')
        groups = {}
        assigned = []

        for event_id, m_hash in min_hashes:
            if event_id in assigned:
                continue
            result = lsh.query(m_hash)
            for item_id in result:
                assigned.append(item_id)
            
            group_id = 'group_'+ str(len(groups))
            text = [stacktrace for (e_id, _, stacktrace) in self.data if e_id == event_id][0]
            groups[group_id] = { 'items': result, 'text': text }

        return groups

def get_parser():
    parser = argparse.ArgumentParser(description='command line utility to monitor error levels using ErrorGUI storage by comparing stacktraces Jaccard similarity')

    parser.add_argument('-u', '--dbUser', help='the database user name', type=str)
    parser.add_argument('-p', '--dbPwd', help='the database password', type=str)
    parser.add_argument('-i', '--interval', help='the interval in days', type=int)

    parser.add_argument('-v', '--version', help='displays the current version', action='store_true')

    return parser

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if not args['dbUser'] or not args['dbPwd'] or not args['interval']:
        parser.print_help()
        return

    dbUser = args['dbUser'].strip()
    dbPwd = args['dbPwd'].strip()
    interval = args['interval']
    
    runner = Runner(dbUser, dbPwd, interval)
    runner.analyze_logs()

if __name__ == '__main__':
    command_line_runner()