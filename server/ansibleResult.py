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
# This scripts is used to analyze the Ansible execution result, and send out mail
# notifications.

# required python modules:
# sys, commands, logging, string, re

import os
import sys
import commands
import logging
import string
import re

def ansible_result(logfilepath,logfilename):
    ## Specify the ansible result log file
    logfile=logfilepath+'/'+logfilename
    job_name=logfile.split('.')[0].split('/')[-1]
    job_success=0
    pattern = re.compile(r'^PLAY RECAP')
    file_object=open(logfile)
    try:
      all_lines=file_object.readlines()
      count = len(all_lines)
      i = 0
      result_set = []
      for line in all_lines:
          updateline = line.strip() 
          i = i + 1
          match = pattern.match(updateline) 
          if match:
             target_line = i
             break	
      ##Get the content under the PLAY RECAP, which contains the ansible execution summary on each node
      for x in range(target_line,count):
	  if all_lines[x] != '\n':
             result_set.append(all_lines[x])
      #print(result_set)
      ##If the unreachable and failed number is both zero, the job is successful.
      for result in result_set:
          result_part=result.split(':')
          #print(result_part)
          item=result_part[1].split('   ')
          #print(item)
          unreachable_item=item[2].split('=')
          #print(unreachable_item)
          failed_item=item[3].split('=')
          #print(failed_item)
          unreachable_result=unreachable_item[1].rstrip('\n').rstrip(' ')
          failed_result=unreachable_item[1].rstrip('\n').rstrip(' ')
          if (unreachable_result=='0') and (failed_result=='0'):	
             job_success=job_success+0
          else:
             job_success=job_success+1
          return job_success
    finally:
		file_object.close()

if __name__ == "__main__":
        ansible_result(sys.argv[1], sys.argv[2], sys.argv[3])
        print(sys.argv[1])
        print(sys.argv[2])
