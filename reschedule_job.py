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
# This script will reschedule an existing job to another time. 
# There is bug with the APScheduler infrastructure, please refer to this website
# for bug details:
# https://github.com/agronholm/apscheduler/issues/174#issuecomment-265703058

import rpyc
import os
import sys
import pytz
from glob import glob
from datetime import datetime, timedelta
from pytz import timezone

from transform_time import *

if len(sys.argv)<4  or sys.argv[1].startswith('-'):
        print 'Use: %s <Env Name> <Job Name> <Job_Time>' % sys.argv[0]
        sys.exit(1)

cur_path=os.getcwd()
searchPath=cur_path + '/jobid'

env_name=sys.argv[1]
job_name=sys.argv[2]
job_org_time=sys.argv[3]
job_reschedule_time=sys.argv[4]

job_time_str=str(job_org_time)[0:-3]
##transform the time to GTM+8
jobtime=trans_time(job_time_str,0)
job_time_format=jobtime.strftime("%Y%m%d%H%M%S")

job_reschedule_time_str=str(job_reschedule_time)[0:-3]
jobresctime=trans_time(job_reschedule_time_str,0)
job_reschedule_time_format=jobresctime.strftime("%Y-%m-%d %H:%M:%S")
##Prepare the JobID file prefix
job_id=env_name+'-'+job_name+'-'+job_time_format
conn = rpyc.connect('localhost', 12345)
##Reschudle the job

job=conn.root.reschedule_job(id=job_id,trigger='date',run_date=job_reschedule_time_format,timezone='Asia/Shanghai')
job_detail=conn.root.get_job(job_id)

print("********************************************")
print("The paused job id is:")
print(job_detail)
print("********************************************")

mail_send_time_utc=trans_time(job_reschedule_time_str,180)
mail_send_time_format=mail_send_time_utc.strftime("%Y-%m-%d %H:%M:%S")
#mail_send_time_format=mail_send_time_utc.strftime("%Y%m%d%H%M%S")
mail_job_id='sendmail-'+env_name+'-'+job_name+'-'+mail_send_time_utc.strftime("%Y%m%d%H%M%S")

job=conn.root.reschedule_job(id=mail_job_id,trigger='date',run_date=mail_send_time_format,timezone='Asia/Shanghai')
mailjob_detail=conn.root.get_job(mail_job_id)

print("The paused mail job id is:")
print(mailjob_detail)
print("********************************************")

conn.close()
