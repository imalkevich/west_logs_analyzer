import cx_Oracle

from datetime import datetime
from .configuration import CONFIGURATION

class FakeRetriever(object):
    def __init__(self, user, pwd):
        self.call_count = 0
        pass

    def get_logs(self, day):
        logs = []
        if self.call_count == 0:
            logs = [
                ('1', day, 'some logs from me'),
                ('2', day, 'some logs from my daughter'),
                ('3', day, 'some logs from my mother'),
                ('4', day, 'some logs from my father')
            ]
        elif self.call_count == 1:
            logs = [
                ('5', day, 'data analytics is hard'),
                ('6', day, 'data analytics is slow'),
                ('7', day, 'data analytics is paid well'),
                ('8', day, 'data analytics is respectful')
            ]
        else:
            logs = [
                ('9', day, 'Cobalt is project with complex module interactions'),
                ('10', day, 'Cobalt is project with complex business rules'),
                ('11', day, 'Cobalt is project with complex deployment'),
                ('12', day, 'Cobalt is project with complex billing')
            ]

        self.call_count+=1

        return logs

class SqlLogsRetriever(object):
    def __init__(self, user, pwd):
        self.connection = self._get_connection_str(user, pwd)

    def _get_connection_str(self, user, pwd):
        config = CONFIGURATION['database']
        CONN_INFO = {
            'host': config['host'],
            'port': config['port'],
            'user': user,
            'psw': pwd,
            'service': config['service']
        }

        CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO)

        return CONN_STR

    def get_logs(self, day):
        partition = 'TIME_{}'.format(day.strftime('%Y%m%d'))

        sql = (
        'SELECT '
            'EVENT_ID, GENERATED_TIMESTAMP, STACKTRACE '
        'FROM '
            'ERRORLOG_DEMO.ERROR_LOG PARTITION ({})'
        'WHERE '
            'APP_NAME_ID = (SELECT APP_NAME_ID FROM ERRORLOG_DEMO.APP_NAME WHERE APP_NAME = \'Website\')'
            'AND PRODUCT_ID IN ( '
                    'SELECT PRODUCT_ID FROM ERRORLOG_DEMO.PRODUCT WHERE PRODUCT IN (\'WESTLAWNEXT-DEMO\', \'WestlawNext-DEMO\', \'WESTLAWNEXT-DEMO\', \'WESTLAW-DEMO\', \'WestlawNext-DEMO\') '
            ') '
            +('and ROWNUM <= 20 ' if CONFIGURATION['is_dev_mode'] == True  else '')+
        'ORDER BY '
            'GENERATED_TIMESTAMP ASC'
        ).format(partition)

        con = cx_Oracle.connect(self.connection)
        cur = con.cursor()
        cur.execute(sql)

        logs = []
        res = cur.fetchall()
        for r in res:
            (event_id, timestamp, stacktrace) = r
            logs.append((event_id, timestamp, stacktrace))
            
        return logs