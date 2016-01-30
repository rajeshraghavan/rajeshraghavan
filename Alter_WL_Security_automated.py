##################################################################################################################################
# This Script will add the group mwss.bi.team and the service account obiee to Weblogic Admnistration Role and to the JMS Module
# Author - rajeshr
# Questions - mwss.bi.team@qualcomm.com
# Date - 08/22/2013
# The script will prompt for Weblogic admin user credentials, admin server name, admin server port and Weblogic domain name.
##################################################################################################################################

import sys
import os
import time as PyTime
from datetime import datetime
import socket

#wlshostname=(socket.gethostname())
wlshostname=sys.argv[1]
wlsport = sys.argv[2]
wlsusrname=sys.argv[3]
wlspassword=sys.argv[4]
svc_acct=sys.argv[5]

def connectwls(wlsusername,wlspassword,wlshostname,wlsport):
    try:
       conncmd1="connect('" + wlsusrname + "', '" + wlspassword + "', '" + wlshostname + ":" + wlsport + "')"
       exec conncmd1
    except:
       print "Couldn't connect to the WLS admin server"

#######
#Main
########

print 'Make sure the correct cacerts with new QC certs has been copied to its location' 


#wlsusrname=raw_input('Enter the Weblogic Username: ')
#wlspassword=raw_input('Enter the Weblogic Password: ')
#wlshostname=raw_input('Enter the Weblogic Admin Server Host name for which the Administrator group needs to be altered: ')
#wlsport=raw_input('Enter the Weblogic Admin Server Port Number: ')
#svc_acct=raw_input('Enter the Service account name that needs BISystem Role: ')

connectwls(wlsusrname,wlspassword,wlshostname,wlsport)

#cmo.getSecurityConfiguration().getDefaultRealm().lookupRoleMapper('XACMLRoleMapper').setRoleExpression(None,'Admin','Grp(Administrators)|Grp(mwss.bi.team)|Usr(obiee)')

conncmd1="cmo.getSecurityConfiguration().getDefaultRealm().lookupRoleMapper('XACMLRoleMapper').setRoleExpression(None,'Admin','Grp(Administrators)|Grp(mwss.bi.team)|Usr(" + svc_acct + ")')"

exec conncmd1

######################################
#Altering the JMS security
######################################

try:

    realm = cmo.getSecurityConfiguration().getDefaultRealm()
    authn = realm.lookupAuthenticationProvider('Qcomldap')

    if authn.userExists("obiee"):
        resourceId = "type=<jms>, application=BipJmsResource"
        authz = realm.lookupAuthorizer('XACMLAuthorizer')
        if authz.policyExists(resourceId):
            print 'Removing the default policy consisting of BISystemUser'
            authz.removePolicy(resourceId)
#           authz.createPolicy(resourceId, 'Usr(obiedwdev)')
            conncmd2="authz.createPolicy(resourceId, 'Usr(" + svc_acct + ")')"
            exec conncmd2
            print "JMS Security has been altered. Added the service account " + svc_acct + " to the JMS policy."
    else:
        print "User " + svc_account + " does not exist ..."

    disconnect()

except:
    dumpStack()
    quit()
