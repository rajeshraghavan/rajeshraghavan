##################################################################################################################################
# Script to alter the changes to make weblogic authenticate against ldap.qualcomm.com:636
# Author - rajeshr
# Questions - mwss.bi.team@qualcomm.com
# Date - 08/31/2012
# The script will prompt for Weblogic admin user credentials, admin server name, admin server port and Weblogic domain name.
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

wlsusrname=raw_input('Enter the Weblogic Username: ')
wlspassword=raw_input('Enter the Weblogic Password: ')
wlshostname=raw_input('Enter the Weblogic Admin Server Host name: ')
wlsport=raw_input('Enter the Weblogic Admin Server Port Number: ')


connectwls(wlsusrname,wlspassword,wlshostname,wlsport)

change_JSSE_SSL()

dom_name=raw_input('Enter ther domain name :  ')


#cd('/SecurityConfiguration/bifoundation_domain/Realms/myrealm')
conncmd1="cd('/SecurityConfiguration/" + dom_name + "/Realms/myrealm/AuthenticationProviders/edir-sd')"
exec conncmd1

cmo.setHost('ldap.qualcomm.com')
cmo.setSSLEnabled(true)
cmo.setPort(636)

save()
activate()

disconnect()
exit()

