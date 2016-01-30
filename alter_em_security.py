##################################################################################################################################
# Script to alter the given username and password in the Credential Store
# Author - rajeshr
# Questions - mwss.bi.team@qualcomm.com
# Date - 09/04/2014
# The script will prompt for Weblogic admin user credentials, admin server name, admin server port.
# Usage - On Exalytics hosts     :  $mw_home/fmw/oracle_common/common/bin/wlst.sh
#         On Regular OBIEE hosts :  $mw_home/oracle_common/common/bin/wlst.sh
###################################################################################################################################

import os
import sys
import time as PyTime
from datetime import datetime


def connectwls(wlsusername,wlspassword,wlshostname,wlsport):
    try:
       conncmd1="connect('" + wlsusrname + "', '" + wlspassword + "', '" + wlshostname + ":" + wlsport + "')"
       exec conncmd1
    except:
       print "Couldn't connect to the WLS admin server, verify if the " + wlshostname + ":" + wlsport + " is accessible."

from weblogic.management.security.authentication import UserReaderMBean
from weblogic.security.providers.authentication import LDAPAuthenticatorMBean
from weblogic.management.security.authentication import MemberGroupListerMBean
from oracle.security.jps.mas.mgmt.jmx.credstore import PortableCredential

wlsusrname=raw_input('Enter the Weblogic Username: ')
wlspassword=raw_input('Enter the Weblogic Password: ')
wlshostname=raw_input('Enter the Weblogic Admin Server Host name for which the credential store needs to be altered: ')
wlsport=raw_input('Enter the Weblogic Admin Server Port Number: ')

csusrname=raw_input('Enter the UserName to be added to BISystemRole : ')

connectwls(wlsusrname,wlspassword,wlshostname,wlsport)

appStripe='obi'

domainCustom()

print "Adding the user " + csusrname + " to BISystem Role"

grantAppRole(appStripe=appStripe, appRoleName='BIAdministrator', principalClass='weblogic.security.principal.WLSGroupImpl', principalName='mwss.bi.team')

print "Addming mwss.bi.team to BIAdministrator role"

cmd1="grantAppRole(appStripe='" + appStripe + "', appRoleName='BISystem', principalClass='weblogic.security.principal.WLSUserImpl', principalName='" + csusrname + "')"

exec cmd1
