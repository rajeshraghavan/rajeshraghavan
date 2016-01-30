##################################################################################################################################
# Script to ete a new provider name edir-sd poiting to edir-sd.qualcomm.com:389
# Author - rajeshr
# Questions - mwss.bi.team@qualcomm.com
# Date - 10/08/2012
# The script will prompt for Weblogic admin user credentials, admin server name, admin server port and Weblogic domain name.
##################################################################################################################################

# User Input Section

wlsusrname=raw_input('Enter the Weblogic Username: ')
wlspassword=raw_input('Enter the Weblogic Password: ')
wlshostname=raw_input('Enter the Weblogic Admin Server Host name: ')
wlsport=raw_input('Enter the Weblogic Admin Server Port Number: ')



cmd1="connect('" + wlsusrname + "', '" + wlspassword + "', '" + wlshostname + ":" + wlsport + "')"

exec cmd1


dom_name=raw_input('Enter ther domain name :  ')

edit()
startEdit()
cd('/')

conncmd1="cd('/SecurityConfiguration/" + dom_name + "/Realms/myrealm')"

exec conncmd1

cmo.createAuthenticationProvider('edir-sd', 'weblogic.security.providers.authentication.NovellAuthenticator')

conncmd2="cd('/SecurityConfiguration/" + dom_name + "/Realms/myrealm/AuthenticationProviders/edir-sd')"
exec conncmd2


cmo.setControlFlag('SUFFICIENT')
cmo.setHost('edir-sd.qualcomm.com')
cmo.setPort(389)
cmo.setPrincipal('uid=wpsadev, ou=people, o=qualcomm')
cmo.setGroupBaseDN('ou=groups, o=qualcomm')
cmo.setUserBaseDN('ou=people,o=qualcomm')
conncmd3="cd('/SecurityConfiguration/" + dom_name + "/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')"
exec conncmd3
cmo.setControlFlag('OPTIONAL')
save()
#set('AuthenticationProviders',jarray.array([ObjectName('Security:Name=myrealmedir-sd'), ObjectName('Security:Name=myrealmDefaultAuthenticator'), ObjectName('Security:Name=myrealmDefaultIdentityAsserter')], ObjectName))
conncmd4="cd('/SecurityConfiguration/" + dom_name + "/Realms/myrealm')"
exec conncmd4
set('AuthenticationProviders',jarray.array([ObjectName('Security:Name=myrealmedir-sd'), ObjectName('Security:Name=myrealmDefaultAuthenticator'), ObjectName('Security:Name=myrealmDefaultIdentityAsserter')], ObjectName))
save()
activate()
print 'edir-sd.qualcomm.com has been configured as a provider on Weblogic server. Restart Admin, Managed servers for the changes to take effect'

