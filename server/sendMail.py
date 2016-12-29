# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Usage:
# Use SMTP to send out mail

# required python modules:
# smtplib, MIMEText, MIMEMultipart

import string

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(to_list, email_title, logfile):

    mail_host = 'SMTP server'
    mail_user = 'SMTP authentication user'
    mail_user_add = 'Mail From,e.g. user@example.com'
    mail_pass = 'SMTP authentication password'
    mail_postfix = 'Mail From domain name,e.g. example.com'
    COMMASPACE = ','
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    to_list = string.split(to_list,",")
    print("********************************************")
    print('Send log file')
    print(email_title)
    print('to the following mail list:')
    print(to_list)
    print("********************************************")
    lf = open(logfile, 'rb')
    log_file = MIMEText(lf.read())
    msg = MIMEMultipart()
    msg['Subject'] = email_title
    msg['From'] = me
    msg['to'] = ','.join(to_list)
    msg.attach(log_file)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user_add,mail_pass)
        s.sendmail(msg['From'],to_list,msg.as_string())
        s.close()
        return True
    except Exception,e:
        print str(e)
    return False

if __name__ == "__main__":
        send_mail(sys.argv[1], sys.argv[2], sys.argv[3])

