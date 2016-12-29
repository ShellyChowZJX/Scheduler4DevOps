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
# The schedule server is based on Python APSchedule Module, use sqlite as backend database
# It provides features like, add/remove/pause/resume jobs, and generate log file, analyze 
# Ansible execution result, and send out the mail notification.

# required python modules:
# sys, commands, subprocess, logging, string, BackgroundScheduler, SQLAlchemyJobStore, rpyc,
#
import os
import sys
import commands
import subprocess
import logging
import string

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

import rpyc
from rpyc.utils.server import ThreadedServer

import ansibleResult
import sendMail
import createLogFile

#LOGDIR=os.path.join(DIRNAME,'log')

logging.basicConfig(level=logging.INFO,
		    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		    datefmt='%Y-%m-%d %H:%M:%S',
		    filename='server.log',
		    filemode='a')

def run_cmd(cmd,logfilepath,logfile):
    log_file = createLogFile.create_file(logfilepath,logfile)
    handle = subprocess.Popen(cmd, stdout=log_file, shell=True)

def mail_log_file(logfilepath,logfilename,maillist):
    ## Specify the ansible result log file
    logfile=logfilepath+'/'+logfilename
    job_name=logfile.split('.')[0].split('/')[-1]

    job_success = ansibleResult.ansible_result(logfilepath,logfilename)

    if (job_success==0):
       email_title = 'Success: ' + job_name
    else:   
       email_title = 'False: ' + job_name
     
    sendMail.send_mail(maillist,email_title,logfile)

class SchedulerService(rpyc.Service):
    def exposed_add_job(self, func, *args, **kwargs):
        return scheduler.add_job(func, *args, **kwargs)
    def exposed_modify_job(self, job_id, jobstore, **changes):
        return scheduler.modify_job(job_id, jobstore, **changes)

    def exposed_reschedule_job(self, job_id, jobstore, trigger=None, **trigger_args):
        return scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)

    def exposed_pause_job(self, job_id, jobstore):
        return scheduler.pause_job(job_id, jobstore)

    def exposed_resume_job(self, job_id, jobstore):
        return scheduler.resume_job(job_id, jobstore)

    def exposed_remove_job(self, job_id, jobstore=None):
        scheduler.remove_job(job_id, jobstore)

    def exposed_get_job(self, job_id):
        return scheduler.get_job(job_id)

    def exposed_get_jobs(self, jobstore=None):
        return scheduler.get_jobs(jobstore)

    def exposed_print_jobs(self, jobstore=None):
        return scheduler.print_jobs(jobstore)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    url = sys.argv[1] if len(sys.argv) > 1 else 'sqlite:///backgroundschedule.sqlite'
    jobstore=scheduler.add_jobstore('sqlalchemy', url=url)
    scheduler.start()
    print('Scheduler server is running now, Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    protocol_config = {'allow_public_attrs': True}
    server = ThreadedServer(SchedulerService, port=12345, protocol_config=protocol_config)
    try:
        server.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
