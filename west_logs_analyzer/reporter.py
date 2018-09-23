import smtplib

from datetime import datetime
from email.message import EmailMessage

from prettytable import PrettyTable

from west_logs_analyzer.configuration import CONFIGURATION

class ErrorEmailNotificator(object):
    def __init__(self, logs, days, groups):
        self.logs = logs
        self.days = days
        self.groups = groups
    
    def _intersection(self, lst1, lst2):
        return list(set(lst1) & set(lst2))

    def _get_log_counts(self, day, group_items):
        items = [event_id for (event_id, timestamp, _) in self.logs if 
            timestamp.year == day.year and timestamp.month == day.month and timestamp.day == day.day]
        counts = len(self._intersection(group_items, items))
        return counts

    def _create_table(self):
        tbl = PrettyTable()

        tbl.field_names = ['#', 'Short text']

        for day in self.days:
            tbl.field_names.append(day.strftime('%m/%d/%Y'))

        for idx, key in enumerate(self.groups):
            row = [idx]
            
            text = self.groups[key]['text']
            row.append(text)

            for day in self.days:
                count = self._get_log_counts(day, self.groups[key]['items'])
                row.append(count)

            tbl.add_row(row)

        return tbl

    def _populate_email_body(self):
        tbl = self._create_table()

        tbl_attr = { 
            'style': 'border: 1px solid black; border-collapse: collapse;',
            'cellpadding': 5,
            'border': 1
        }

        body = 'Report generated on {}<br/>'.format(datetime.now().strftime('%Y-%m-%d %H:%M'))

        body += '<br/>'
        body += tbl.get_html_string(attributes=tbl_attr)
        body += '<br/><br/>'

        body += 'Thanks'

        return body


    def send_notification(self):
        body = self._populate_email_body()

        config = CONFIGURATION['email']

        msg = EmailMessage()

        msg['Subject'] = config['subject_template'].format(start = self.days[0].strftime('%Y-%m-%d'), 
            end = self.days[len(self.days) - 1].strftime('%Y-%m-%d'))
        msg.set_content(body)
        msg['From'] = config['from']
        msg['To'] = config['to']
        msg.replace_header('Content-type', 'text/html')

        server = smtplib.SMTP(config['relay_server'])
        server.ehlo()
        server.send_message(msg)
        server.quit()



