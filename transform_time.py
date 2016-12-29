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
# This script is used to transform the time to GTM+8 Asia/Shanghai time.
# example, the time from UCD is the UNIX format, like 1482376500000, it is actual
# time is 12/22/2016, 11:15:00 AM. Using pytz can do the time transformation.
# scheduler_time is the time need be transfromed, like 1482376500000
# delta_time is the time used to add positive/negative time to the scheduler_time.
# 

# Usage example:
# trans_time(1482376500000, 60)

# required python modules:
# sleep, datetime, timedelta, pytz

from time import sleep

from datetime import datetime, timedelta
from pytz import timezone
import pytz
import sys
import os

def trans_time(scheduler_time,delta_time):
  ##schedule time  is the Beijing time GMT+8.
  ## Transform the time to UTC 
  trimtime=str(scheduler_time)[0:-3]
  utc = pytz.utc
  utc_dt = utc.localize(datetime.utcfromtimestamp(int(trimtime)))
  utc_dt.strftime("%Y-%m-%d %H:%M:%S")
  
  ##Transform the timezone to 'Asia/Shanghai'
  sh_tz=timezone('Asia/Shanghai')
  sh_utc_dt=utc_dt.astimezone(sh_tz)
   
  ##delta time is used to set the mail send time
  time = int(delta_time)
  schedule_delta_time = sh_utc_dt+timedelta(seconds=time)
  #print(schedule_delta_time)
  return schedule_delta_time

if __name__ == "__main__":
     trans_time(sys.argv[1], sys.argv[2])
     #print(sys.argv[1])
     #print(sys.argv[2])
