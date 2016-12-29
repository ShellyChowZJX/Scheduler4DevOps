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
# This script will submit a schedule job to the schedule server(Currently, the 
# timezone is set as GMT+8/Asia_Shanghai), and run the job
# on the remote system. It generates a specific job id for other schdule jobs.
# env_name is the environment that schedule will run on. It is used to generate 
# the job id.
# task_name is the action that the schedule will execute. It is used to generate 
# the job id.
# scheduler_time is the time when the job is scheduled to run

# required python modules:
# rpyc, pytz, datetime, sleep, timedelta

from time import sleep

import rpyc
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import sys
import os

import transform_time

if len(sys.argv)<4  or sys.argv[1].startswith('-'):
        print 'Use: %s <environment name> <task name> <schedule time> ' % sys.argv[0]
        sys.exit(1)

env_name=sys.argv[1]
task_name=sys.argv[2]
scheduler_time=sys.argv[3]
###############################################################
##Run Ansible command here
###############################################################

scheduler_time_utc=transform_time.trans_time(scheduler_time,0)
scheduler_time_format=scheduler_time_utc.strftime("%Y-%m-%d %H:%M:%S")

print("********************************************")
print("The actual scheduler time:") 
print(scheduler_time_format)
print("********************************************")

cmd = ''

curPath=os.getcwd()
logfilepath=curPath+'/log'
logfilename=env_name+'-'+task_name+'-'+scheduler_time_utc.strftime("%Y%m%d%H%M%S")+'.log'

jobid=env_name+'-'+task_name+'-'+scheduler_time_utc.strftime("%Y%m%d%H%M%S")
print("********************************************")
print("The add job id:")
print(jobid)
print("********************************************")
#Add the Task as job to the BackgroundScheduler
conn = rpyc.connect('localhost', 12345)
job = conn.root.add_job(func='server:run_cmd', id=jobid, trigger='date', run_date=scheduler_time_format, timezone='Asia/Shanghai', args=(cmd,logfilepath,logfilename))

###############################################################
##send mail to operation team 3 min later after the schedule is
##finished.
###############################################################

mail_send_time_utc=transform_time.trans_time(scheduler_time,180)
mail_send_time_format=mail_send_time_utc.strftime("%Y-%m-%d %H:%M:%S")
##Set the mail receiver Email address
mail_list='user1@example.com' 
mail_job_id='sendmail-'+env_name+'-'+task_name+'-'+mail_send_time_utc.strftime("%Y%m%d%H%M%S")
print("The send mail job id:")
print(mail_job_id)
print("********************************************")
job = conn.root.add_job(func='server:mail_log_file', id=mail_job_id, trigger='date', run_date=mail_send_time_format, timezone='Asia/Shanghai', args=(logfilepath,logfilename,mail_list))

print("The task is scheduled, please check your mail box 3 mintues later of the schedule time")
print("********************************************")

conn.close()
