#########################################################################################
# This script uploads the latest RPD available in the MUDE to TST and bounced the server
# Author - rajeshr
# USAGE: wlst Migrate_RPD_alt.py Target_Instance Weblogic_Admin_Server_url rpd_path rpd_pwd WLS_ADMIN_URL 
# Example : wlst Migrate_RPD_alt.py EDWTST obiedwtst01.qualcomm.com:7001 /prj/obiee/OBIPOC11G/Repository/SampleAppLite_BI0001.rpd Password123 obipoc11g1.qualcomm.com:7001
# For questions email mwss.bi.team@qualcomm.com
#########################################################################################

#connect(userConfigFile='E:/11g-Patch-Raj/OBIPOC11GDEV/obipoc11g_weblogic_userconfigfile.secure',userKeyFile='E:/11g-Patch-Raj/OBIPOC11G/obipoc11g_weblogic_userkeyfile.secure',url='obipoc11g1.qualcomm.com:7001')

#connect(userConfigFile='//ziplock/obiee-dev/QTMDEV/credentials/QTMDEV_weblogic_configfile.secure',userKeyFile='//ziplock/obiee-dev/QTMDEV/credentials/QTMDEV_weblogic_keyfile.secure',url='obiqtmdev1.qualcomm.com:7001')
 
import sys
import os
from time import sleep
from java.util import Date

tgt_inst = sys.argv[1]
WLS_URL = sys.argv[2]
rpd_path = sys.argv[3]
rpd_pwd = sys.argv[4]

argsLen = len(sys.argv)
if argsLen -1 != 4:
   sys.exit("The number of parameters passed to the RPD migration jython script is not 4. Please verify the number of parameters and run the script again")


conncmd="connect(userConfigFile='//ziplock/obidev/" + tgt_inst + "/credentials/" + tgt_inst + "_configfile.secure',userKeyFile='//ziplock/obidev/" + tgt_inst + "/credentials/" + tgt_inst + "_keyfile.secure',url='" + WLS_URL + "')"
print conncmd
exec conncmd

domainCustom()

cd('/')

print Date() , ': Start: Locking the OBIEE Environment'

cd ('oracle.biee.admin/oracle.biee.admin:type=BIDomain,group=Service')

print 'cd done'

# Locking the Environment

invoke('lock', jarray.array([], java.lang.Object), jarray.array([], java.lang.String))

print 'Completed: Locking the OBIEE Environment'

print Date() , ': Completed: Locking the OBIEE Environment'


# Report the Repository Details 

cd('../oracle.biee.admin:type=BIDomain.BIInstance.ServerConfiguration,biInstance=coreapplication,group=Service')

Rep_Name=get('RepositoryName')

Rep_Location= get('RepositorySharedLocation')

#print Date() ,': The RPD with the name ' +Rep_Name + ' under the location ' +Rep_Location +' will be overwritten'

print Date() ,': The RPD with the name ', Rep_Name, ' under the location ', Rep_Location ,' will be overwritten'

print Date() , ': Uploading the RPD'

#Upload the Repository

#invoke( 'uploadRepository', jarray.array(['/prj/obiee/OBIPOC11G/Repository/SampleAppLite_BI0001.rpd','Admin123'],java.lang.Object), jarray.array(['java.lang.String', 'java.lang.String'],java.lang.String))

invoke( 'uploadRepository', jarray.array([rpd_path,rpd_pwd],java.lang.Object), jarray.array(['java.lang.String', 'java.lang.String'],java.lang.String))

print Date() , ': RPD Upload completed successfully'

cd ('../oracle.biee.admin:type=BIDomain,group=Service')

print Date() , ': Committing the changes now'

invoke('commit', jarray.array([], java.lang.Object), jarray.array([], java.lang.String)) 

print Date() , ': Changes committed'

#Bounce the environment
cd('../oracle.biee.admin:type=BIDomain,group=Service')

biinstance_status = get('BIInstances')
biinstance = biinstance_status[0]
cd('../'+biinstance.toString())
servicestatus=get('ServiceStatus')

print Date() , ': OBIEE Environment - ServiceStatus: ' + servicestatus

print Date() , 'RPD upload complete. Bouncing OBIEE Now'

#invoke('stop', jarray.array([], java.lang.Object), jarray.array([], java.lang.String))
servicestatus=get('ServiceStatus')
print Date() , 'OBIEE Environment - ServiceStatus: ' + servicestatus

#invoke('start', jarray.array([], java.lang.Object), jarray.array([], java.lang.String))

servicestatus=get('ServiceStatus')

print Date() , ' OBIEE Environment - ServiceStatus: ' + servicestatus

for x in xrange(0,5):
     servicestatus=get('ServiceStatus')


     if servicestatus=='FULLY_STARTED':
        print Date() ,'Service started'
        disconnect()
        exit()
     else:
        sleep(0.20)

print Date() ,'The service did not startup, please look into this'

disconnect()

exit()








