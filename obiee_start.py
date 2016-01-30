# This scripts expects the following arguments:
#This scripts stops all the Managed Servers in a Weblogic domain
#Author - rajeshr
#Questions - mwss.bi.team@qualcomm.com
# 1. wls.host (localhost)
# 2. wls.port (7001)
# 3. wls.user  (user1)
# 4. wls.password  (password1)
#Date - 10/17/2013
#####################################################################################################
import sys
import os
# Check the arguments to this script are as expected.
# argv[0] is script name.
argLen = len(sys.argv)
if argLen -1 != 4:
    print "ERROR: got ", argLen -1, " args."
    print "USAGE: wlst_stop_start.cmd wls_stop_start_obi.py WLS_HOST WLS_PORT WLS_USER WLS_PASSWORD"
    print "   eg: wlst_stop_start.cmd wls_stop_start_obi.py localhost 7001 user1 password1" 
    exit()
WLS_HOST = sys.argv[1]
WLS_PORT = sys.argv[2]
WLS_USER = sys.argv[3]
WLS_PW = sys.argv[4]
print 'Connecting to '+ WLS_HOST+ ':' + WLS_PORT + ' as user: ' + WLS_USER + ' ...'
# Connect to WLS
connect(WLS_USER, WLS_PW, WLS_HOST+ ':' + WLS_PORT);
print 'Connecting to Domain ...'
domainCustom()
cd ('oracle.biee.admin')
print 'Connecting to BIDomain MBean ...'
cd ('oracle.biee.admin:type=BIDomain,group=Service')
biinstances = get('BIInstances')
biinstance = biinstances[0]
print 'Connecting to BIInstance MBean ...'
cd ('..')
cd (biinstance.toString())
servicestatus=get('ServiceStatus')
print 'BIInstance MBean; ServiceStatus: ' + servicestatus
#print 'Calling stop ...'
#objs = jarray.array([], java.lang.Object)
#strs = jarray.array([], java.lang.String)
#invoke('stop', objs, strs)
#servicestatus=get('ServiceStatus')
#print 'BIInstance MBean; ServiceStatus: ' + servicestatus
print 'Calling start ...'
objs = jarray.array([], java.lang.Object)
strs = jarray.array([], java.lang.String)
invoke('start', objs, strs)
servicestatus=get('ServiceStatus')
print 'BIInstance MBean; ServiceStatus: ' + servicestatus
exit()