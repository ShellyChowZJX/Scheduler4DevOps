# DevScheduler
# DevScheduler

This project is combined APScheduler, Ansible, IBM UrbanCode Deploy(aka, UCD) to schedule a task which will be run on SoftLayer environment.
The IBM UrbanCode Deploy(aka, UCD) will provide a friendly UI to manage SoftLayer environment, submit the schedule task. The APScheduler will make sure the job run at the scheduled time. The Ansible scripts will execute the actual commands on SoftLayer environment. In this project, it has serveral jobs, like add/remove/pause/resume schedule job.

The architecture of this project is as follow:
1. The server.py in server folder is acted as the server, which receives the requests from client, and stores the job in the sqilite database. When the scheduled job is run, it will  generate log file, send out the mail notification.
2. The scripts of add_job.py, pause_job.py, remove_job.py, resume_job.py will run as the client request, send the schedule job request to the server.
3. The files in ansible_scripts folder will do the actual command execution on SoftLayer environment.
4. The shell scripts mainly focus on receiving parameters from UCD, and update them to the Scheduler.

The contributors for this project are:
thinkingpad@gmail.com
cuiliquan@126.com
junxia0128@gmail.com
