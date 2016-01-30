#!/usr/bin/python


import sys
import smtplib

sender = 'TTAdmin@exalytics2.qualcomm.com'
#receivers = ['rajeshr@qualcomm.com', 'mohand@qualcomm.com']
receivers = ['ps.bi.sd.page@qualcomm.com']
#receivers = sys.argv[2]
#subject = sys.argv[3]
#message = sys.argv[3]


message = """From: TTAdmin <TTAdmin@exalytics2.qualcomm.com>
To: ps.bi.sd.page@qualcomm.com
Subject: TimesTen PRD Database unloaded from RAM

TimesTen PRD Database unloaded from RAM, verify on the host exalytics2
"""

try:
   smtpObj = smtplib.SMTP('smtphost.qualcomm.com')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"
