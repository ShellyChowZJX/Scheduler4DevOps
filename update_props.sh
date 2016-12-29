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
# This script is used to get the parameters from UCD, and update the parameter to
# Schedule scripts.
# COMMOND is the parameter tells scheduler what action it will execute.
# CCINAME is the SoftLayer CloudLayer Computing Instances(CCI).
# ENRIRONMENT is the application environment.
# MAILTOLIST is the mail list who will receive the scheduler notification.

#!/bin/bash
UpdatePythonProps()
{
   BaseScriptDir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
   CMD=$1
   CCINAME=$2
   ENRIRONMENT=$3
   MAILTOLIST=$4

   pythonFile=$BaseScriptDir/add_job.py
   echo $pythonFile
   cmd_task="task"

   ansibleHosts=$BaseScriptDir/ansible_scripts/hosts
   ansibleRole=""

   if [ "$CMD" = "Stop_Liberty_Server" ];then
      cciName=`echo ${CCINAME##*-}`
      envName=$ENRIRONMENT-$cciName
      ansibleRole=$BaseScriptDir/ansible_scripts/stop_liberty_server.yml
      cmd_task="ansible-playbook -i ${ansibleHosts} ${ansibleRole} --extra-vars "hosts=${envName}""
   fi
   sed -i "s%cmd = .*%cmd = '$cmd_task'%" $pythonFile
   sed -i "s/mail_list=.*/mail_list='$MAILTOLIST'/" $pythonFile
}

usage()
{
       echo "Usage: $0 -m -h -e -l"
       echo "   -m means to specify the command"
       echo "   -h means to specify the CCI"
       echo "   -e means to specify the environment"
       echo "   -l means to specify the mail to list"
}
while getopts :m:h:e:l: OPT
do
       case "$OPT"
       in
              m) COMMOND=$OPTARG
                          ;;
              h) CCINAME=$OPTARG
                          ;;
              e) ENRIRONMENT=$OPTARG
                          ;;
	      l) MAILTOLIST=$OPTARG
			  ;;
             \?) usage
                 exit 1;;
       esac
done
if [ $# -eq 8 ]
then
    UpdatePythonProps $COMMOND $CCINAME $ENRIRONMENT $MAILTOLIST
else
    usage
fi

