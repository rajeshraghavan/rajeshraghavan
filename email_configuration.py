########################################################################################################
# This script updates the email sender Display Name, SMTP server, and Email Display name of sender
# Author - rajeshr
# Questions - mwss.bi.team@qualcomm.com
# Date - 01/21/2015
# Usage - $mw_home/oracle_common/common/bin/wlst.sh email_configuration.py
#######################################################################################################

def connectwls(wlsusername,wlspassword,wlshostname,wlsport):
    try:
       conncmd1="connect('" + wlsusrname + "', '" + wlspassword + "', '" + wlshostname + ":" + wlsport + "')"
       exec conncmd1
    except:
       print "Couldn't connect to the WLS admin server"

import sys
import os
 
# Check the arguments to this script are as expected.

newDisplayName = raw_input('Enter the new EMAIL Display Name: ')
smtphostname = raw_input('Enter the valid SMTP host name: ')
#smtpport = raw_input('Enter the valid SMTP port: ') 
newEmailAddr = raw_input('Enter the sender email address: ')
 
wlsusrname=raw_input('Enter the Weblogic Username: ')
wlspassword=raw_input('Enter the Weblogic Password: ')
wlshostname=raw_input('Enter the Weblogic Admin Server Host name: ')
wlsport=raw_input('Enter the Weblogic Admin Server Port Number: ')

connectwls(wlsusrname,wlspassword,wlshostname,wlsport)
 
print 'Connecting to Domain ...'
domainCustom()
cd ('oracle.biee.admin')
print 'Connecting to BIDomain MBean ...'
cd ('oracle.biee.admin:type=BIDomain,group=Service')
#bidomain=cmo
 
print 'Calling lock ...'
objs = jarray.array([], java.lang.Object)
strs = jarray.array([], java.lang.String)
invoke('lock', objs, strs)
 
biinstances = get('BIInstances')
biinstance = biinstances[0]
 
print 'Connecting to BIInstance MBean ...'
cd ('..')
cd (biinstance.toString())
 
servicestatus=get('ServiceStatus')
print 'BIInstance MBean; ServiceStatus: ' + servicestatus
 
biemailbean = get('EmailConfiguration')
print 'Connecting to BIInstance Email MBean ...'
cd ('..')
cd (biemailbean.toString())
 
oldDisplayName=get('SenderDisplayName')
print 'Existing email displayname is: ' + oldDisplayName
print 'Changing email displayname to: ' + newDisplayName + ' ...'
set('SenderDisplayName', newDisplayName)

oldsmtpserver=get('SmtpServer')
print 'Changing the smtp server name from ' + oldsmtpserver + ' to ' + smtphostname
set('SmtpServer', smtphostname)

#set('SmtpServerPort', smtpport)

oldEmailAddr=get('SenderEmailAddress')
print 'Changing the Email Address from ' + oldEmailAddr + ' to ' + newEmailAddr

set('SenderEmailAddress', newEmailAddr)
  
print 'Calling commit ...'
cd ('..')
cd ('oracle.biee.admin:type=BIDomain,group=Service')
objs = jarray.array([], java.lang.Object)
strs = jarray.array([], java.lang.String)
invoke('commit', objs, strs)
 
print 'Committed OK'
 
exit()
