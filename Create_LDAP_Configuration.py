##################################################################################################################################
# Script to alter the changes to make weblogic authenticate against ldap.qualcomm.com:636
# Author - rajeshr
# Questions - mwss.bi.team@qualcomm.com
# Date - 07/09/2013
# The script will take 4 paramerters admin user credentials, admin server name, admin server port and Weblogic domain name.
##################################################################################################################################

def connectwls(wlsusername,wlspassword,wlshostname,wlsport):
    try:
       conncmd1="connect('" + wlsusrname + "', '" + wlspassword + "', '" + wlshostname + ":" + wlsport + "')"
       exec conncmd1
    except:
       print "Couldn't connect to the WLS admin server"


def server_state(svrName):
    sstate = 'UNKNOWN'
    try:
        myTree = currentTree()
        domainRuntime()
        #cd( '/ServerLifeCycleRuntimes/' + server_name)
        #sstate = get('State')
        sstate = cmo.lookupServerLifeCycleRuntime(svrName).getState()
        myTree()
    except:
        print 'Exception while trying to get ServerRuntimeMBean'
        myTree()
    return sstate

def change_JSSE_SSL():
    srvs = cmo.getServers()
    edit()
    startEdit() 
    for server in srvs:
        try:
            cd('/')
            conncmd2="cd('Servers/" + server.getName() + "/SSL/" + server.getName() + "')"
            exec conncmd2
            cmo.setJSSEEnabled(true) 
            print "JSEE SSL has been enabled on the server " + server.getName()
            save()
        except:
            print "Couldn't connect to server " + server.getName()

#############################################################
#Main
#############################################################

#wlsusrname=raw_input('Enter the Weblogic Username: ')
#wlspassword=raw_input('Enter the Weblogic Password: ')
#wlshostname=raw_input('Enter the Weblogic Admin Server Host name: ')
#wlsport=raw_input('Enter the Weblogic Admin Server Port Number: ')
import os
from java.util import Date

log_path = '/local/mnt/obiee/Oracle_Inventory/logs/'
name_of_file = 'post_install_log'
logfile = os.path.join(log_path, name_of_file+".txt")
Log_file = open(logfile, "a")

wlshostname=sys.argv[1]
wlsport = sys.argv[2]
wlsusrname=sys.argv[3]
wlspassword=sys.argv[4]
dom_name=sys.argv[5]

connectwls(wlsusrname,wlspassword,wlshostname,wlsport)

change_JSSE_SSL()

#dom_name=raw_input('Enter ther domain name :  ')

conncmd1="cd('/SecurityConfiguration/" + dom_name + "/Realms/myrealm')"
exec conncmd1
try:
    cmo.createAuthenticationProvider('Qcomldap', 'weblogic.security.providers.authentication.NovellAuthenticator')
    conncmd2="cd('/SecurityConfiguration/" + dom_name + "/Realms/myrealm/AuthenticationProviders/Qcomldap')"
    exec conncmd2
    Log_file.write("=========================================================== \n")
    Log_file.write(str(Date()) + ': Completed ctreating the LDAP provider \n')
    cmo.setControlFlag('SUFFICIENT')
    cmo.setHost('ldap.qualcomm.com')
    cmo.setSSLEnabled(true)
    cmo.setPort(636)
    cmo.setPrincipal('uid=wpsadev, ou=people, o=qualcomm')
    cmo.setGroupBaseDN('ou=groups, o=qualcomm')
    cmo.setUserBaseDN('ou=people,o=qualcomm')
    conncmd3="cd('/SecurityConfiguration/" + dom_name + "/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')"
    exec conncmd3
    cmo.setControlFlag('OPTIONAL')
    save()

    conncmd4="cd('/SecurityConfiguration/" + dom_name + "/Realms/myrealm')"
    exec conncmd4
    set('AuthenticationProviders',jarray.array([ObjectName('Security:Name=myrealmQcomldap'), ObjectName('Security:Name=myrealmDefaultAuthenticator'), ObjectName('Security:Name=myrealmDefaultIdentityAsserter')], ObjectName))
    save()
    activate()
    Log_file.write(str(Date()) + ': Completed ctreating the LDAP provider \n')
    disconnect()
    exit()
except:
    Log_file.write(str(Date()) + ": Unable to create the LDAP provider check the log \n")
    disconnect()
    exit()
