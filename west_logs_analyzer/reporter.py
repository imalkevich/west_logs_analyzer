import os
import smtplib

from datetime import datetime
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from prettytable import PrettyTable

from west_logs_analyzer.configuration import CONFIGURATION

class ErrorEmailNotificator(object):
    def __init__(self, days, results, image):
        self.days = days
        self.results = results
        self.image = image

    def _attach_file(self, file_name):
        part = MIMEBase('application', 'octect-stream')
        part.set_payload(open(file_name, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=%s' % os.path.basename(file_name))
        return part

    def _create_table(self):
        tbl = PrettyTable()

        if self.results is None or len(self.results) == 0: 
            return tbl

        tbl.field_names = ['#', 'Short text']

        (_, _, errors) = self.results[0]
        for (day, _) in errors:
            tbl.field_names.append(day.strftime('%m/%d/%Y'))

        for (idx, text, errors) in self.results:
            row = [idx, text]

            for (_, count) in errors:
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

        msg = MIMEMultipart()

        msg['Subject'] = config['subject_template'].format(start = self.days[0].strftime('%Y-%m-%d'), 
            end = self.days[len(self.days) - 1].strftime('%Y-%m-%d'))
        #msg.set_content(body)
        msg['From'] = config['from']
        msg['To'] = config['to']
        msg.attach(self._attach_file(self.image))
        msg.attach(MIMEText(body, 'html'))
        #msg.replace_header('Content-type', 'text/html')

        server = smtplib.SMTP(config['relay_server'])
        server.ehlo()
        server.send_message(msg)
        server.quit()



