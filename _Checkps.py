#!/usr/bin/python
##################################################################################################################
#### remove all the outside whitespace including \n with line.strip()
#### The "int(time_items[-2])" , we have used "int" function to convert the number to an integer
#### The "re.split('-|:')" rejex been used to search and split out the ":" & "-" from the os etime= output \
#### The "re.search(".*[\/|\s]+(rm)\s+", line)" , this will catch the string "rm" 
#### and separate the element in the list.
#### the "line.strip()"  fuction is Just been used to remove all the outside whitespace including \n.
#### Author : Karn Kumar (karn@cadence.com).
#### V.01, 5/15/2017
#### V.02, 5/19/2017 .. added redirection capability and sendmail.
##################################################################################################################
from subprocess import Popen, PIPE
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import socket
import sys
import os
import re

hst_name = (socket.gethostname())
def checK_ps():
    ps = subprocess.Popen(['ps', '-eo' 'pid,user,args,etime='], stdout=subprocess.PIPE)
    output = ps.communicate()[0]
    for line in output.splitlines():
	 #if len(re.findall('\\b'+line+'\\b', "rm", flags=re.IGNORECASE))>0:
	 result = re.search(".*[\/\s]+(rm)\s+", line)
	 #result = re.search(".*[\/|\s]+(rm)\s+", line)
	 if result:
             time_items = re.split('-|:',(line.split(' ')[-1]))
             time_len = len(time_items)
             print_stdout = sys.stdout
             print_output = open('/tmp/ps_msg', 'a')
             sys.stdout = print_output
             if  time_len == 4:
                 print "Alert rm is running longer on the host",hst_name,time_items[0],"days:" + "\n" + line.strip()
                 print "" 

             #elif time_len == 3:
             elif time_len == 3 and int(time_items[-3]) >= 02:
                 print "Alert rm is running longer on the host",hst_name,time_items[-3],"hours:" + "\n" +  line.strip()
                 print ""

             elif time_len == 2 and int(time_items[-2]) >= 00:
                 print "Alert rm is running longer on the host",hst_name,time_items[-2],"minutes:" + "\n" + line.strip()
                 print ""

             sys.stdout = print_stdout
             print_output.close()
checK_ps()

############ Process capturing part done above #################
############ File comparison & sendmail part starts here ########
def ps_Mail():
    filename = "/tmp/ps_msg"
    f = file(filename)
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        mailp = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
        msg = MIMEMultipart('alternative')
        msg['To'] = "karn@cadence.com"
        msg['Subject'] = "Uhh!! Unsafe rm process Seen"
        msg['From'] = "psCheck@cadence.com"
        msg1 = MIMEText(f.read(),  'text')
        msg.attach(msg1)
        mailp.communicate(msg.as_string())
ps_Mail()
###########  Clean the file after Sending an E-mail  ############
os.unlink("/tmp/ps_msg")
