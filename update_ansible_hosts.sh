# permission is hereby granted, free of charge, to any person obtaining a copy
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
# It focus on the SoftLayer CloudLayer Computing Instances(CCI), auto generate the current 
# living instances info, populate the CCI info into Ansible hosts file, and categorize it.

# ENRIRONMENT is the application environment.
# MAILTOLIST is the mail list who will receive the scheduler notification.

#!/bin/bash

UpdateBuildProps()
{
   BaseScriptDir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
   CCINAME=$1
   ENVIRONMENT=$2
   ansibleHosts="$BaseScriptDir/ansible_scripts/hosts"
   ansible_ssh_user=<ssh user>
   ansible_ssh_key=<ssh key>
   NODEIP=`/usr/bin/slcli vs list |grep $CCINAME |awk '{print $4}'`
   if [ -z $NODEIP ]
   then
       echo "No IP for $CCINAME was found"
       exit 1
   else
        echo $CCINAME $NODEIP
   fi
   if [[ $CCINAME == *-*-* ]]
   then
        echo "The hostname $CCINAME comply naming conversion"
        NODETYPE=`echo $CCINAME | awk -F'-' '{print $NF}'`
        NODETYPE=`echo $NODETYPE | cut -c1-2`
        case $NODETYPE in
          ws |WS | Web| WEB)
	    echo [$ENVIRONMENT-ws] >> $ansibleHosts
	    echo $NODEIP "ansible_ssh_user=$ansible_ssh_user ansible_ssh_private_key_file=$ansible_ssh_key" >> $ansibleHosts
            ;;
          ap | AP | App | APP) 
	    echo [$ENVIRONMENT-ap] >> $ansibleHosts
	    echo "*** This is AP node*********************"  
            echo $NODEIP "ansible_ssh_user=$ansible_ssh_user ansible_ssh_private_key_file=$ansible_ssh_key" >> $ansibleHosts
	    ;;
          db | DB | Data | DATA) 
            echo [$ENVIRONMENT-db] >> $ansibleHosts
            echo $NODEIP "ansible_ssh_user=$ansible_ssh_user ansible_ssh_private_key_file=$ansible_ssh_key" >> $ansibleHosts
            ;;
         esac
   else
        echo "The hostname $CCINAME didn't comply the naming conversion"
        NODETYPE=`echo $CCINAME | awk -F'-' '{print $NF}'`
        case $NODETYPE in
          ws |WS | Web| WEB)
            echo [$ENVIRONMENT-ws] > $ansibleHosts
            echo $NODEIP "ansible_ssh_user=$ansible_ssh_user ansible_ssh_private_key_file=$ansible_ssh_key" >> $ansibleHosts
	    ;;
          ap | AP | App | APP)
            echo [$ENVIRONMENT-ap] >> $ansibleHosts
            echo $NODEIP "ansible_ssh_user=$ansible_ssh_user ansible_ssh_private_key_file=$ansible_ssh_key" >> $ansibleHosts
	    ;;
          db | DB | Data | DATA)
            echo [$ENVIRONMENT-db] >> $ansibleHosts
            echo $NODEIP "ansible_ssh_user=$ansible_ssh_user ansible_ssh_private_key_file=$ansible_ssh_key" >> $ansibleHosts
            ;;
       esac
     
fi
}

SearchCCIlist()
{
   CCINAMELIST=$1
   ENVIRONMENT=$2
   
   BaseScriptDir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
   ansibleHosts="$BaseScriptDir/ansible_scripts/hosts"
   CCINAMELIST=`echo $CCINAMELIST | tr -s ',' ' '`
   echo "" > $ansibleHosts
   for CCINAME in $CCINAMELIST
   do

       if [[ $CCINAME == "NONE" || -z $CCINAME ]]
       then
           echo "Please specify instance name ..."
       else
           /usr/bin/slcli vs list |grep $CCINAME
           if [ $? -eq 0 ]
           then
                echo "Update build properties for  ${CCINAME} ..."
                UpdateBuildProps ${CCINAME} ${ENVIRONMENT}
 else
                echo "No such cci instance ${CCINAME}"
           fi
       fi
   done
   echo [$ENVIRONMENT:children] >> $ansibleHosts
   echo [$ENVIRONMENT-ap] >> $ansibleHosts
   echo [$ENVIRONMENT-db] >> $ansibleHosts
   echo [$ENVIRONMENT-ws] >> $ansibleHosts
}

usage()
{
       echo "Usage: $0 [-l cci instance name list ]"
       echo "   -l means to specified the list of cci name"
       echo "   -e means to specify the environment name"
}
while getopts :l:e: OPT
do
       case "$OPT"
       in
              l) CCINAMELIST=$OPTARG
                          ;;
	      e) ENVIRONMENT=$OPTARG
			  ;;
             \?) usage
                 exit 1;;
       esac
done
if [ $# -eq 4 ]
then
    SearchCCIlist $CCINAMELIST $ENVIRONMENT
else
    usage
fi
