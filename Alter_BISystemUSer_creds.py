##################################################################################################################################
# Script to alter the given username and password in the Credential Store
# Author - rajeshr
# Questions - mwss.bi.team@qualcomm.com
# Date - 09/04/2014
# The script will prompt for Weblogic admin user credentials, admin server name, admin server port.
# Usage - On Exalytics hosts     :  $mw_home/fmw/oracle_common/common/bin/wlst.sh
#         On Regular OBIEE hosts :  $mw_home/oracle_common/common/bin/wlst.sh 
###################################################################################################################################

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

csusrname=raw_input('Enter the credential store UserName: ')
cspwd=raw_input('Enter the credential store Password: ')

connectwls(wlsusrname,wlspassword,wlshostname,wlsport)

domainCustom()

#cd('com.oracle.jps:type=JpsCredentialStore')
#invoke('setPortableCredential', jarray.array([map, key, cd],java.lang.object), java.lang.String, java.lang.String, javax.management.openmbean.CompositeData)

updateCred(map="oracle.bi.system",key="system.user",user=csusrname,password=cspwd,desc="The Credential Store instance config MXBean.")

print 'Credential store has been updated with the user ' + csusrname + ' and its corresponding password' 
