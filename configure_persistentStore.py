###########################################################################################
#This scripts migrates the persistent stores corresponding to both the nodes in cluster
#Author - rajeshr
#Questions - mwss.bi.team@qualcomm.com
#Date - 06/19/2014
#Usage - $MW_HOME/oracle_common/common/bin/wlst.sh configure_persistentStore.py
###########################################################################################
import os
import getpassword


def connectwls(wlsusername,wlspassword,wlshostname,wlsport):
    try:
       conncmd1="connect('" + wlsusrname + "', '" + wlspassword + "', '" + wlshostname + ":" + wlsport + "')"
       exec conncmd1
    except:
       print "Couldn't connect to the WLS admin server"


wlsusrname=raw_input('Enter the Weblogic Username: ')
wlspassword=getpassword.getpassword('Enter the password for ' + wlsusrname)
wlshostname=raw_input('Enter the Weblogic Admin Server Host name: ')
wlsport=raw_input('Enter the Weblogic Admin Server Port Number: ')
instName=raw_input('Enter the instance Name: ')

instName=raw_input('Enter the instance Name: ')

pstore_path="/prj/obiee" + instName + "/persistent_store"
print pstore_path
JmsS_path=pstore_path + "/BipJmsStore"
print JmsS_path
Jrfws_path=pstore_path + "/JRFWSAsyncFileStore"
print Jrfws_path
if not os.path.exists(pstore_path):
  try:
     os.makedirs(pstore_path)
  except:
     print 'Could not create the path ' + pstore_path
  try:
     os.makedirs(JmsS_path)
  except:
     print 'Could not create the path ' + JmsS_path
  try:
     os.makedirs(Jrfws_path)
  except:
     print 'Could not create the path ' + Jrfws_path


cd('/FileStores/BipJmsStore_auto_1')

conncmd1="cd('/prj/obiee/" + instName + "/persistent_store/BipJmsStore')"
exec conncmd1
conncmd2="cmo.setDirectory('/prj/obiee/" + instName + "/persistent_store/BipJmsStore')"
exec conncmd2
cmo.setSynchronousWritePolicy('Direct-Write')
save()

cd('/FileStores/BipJmsStore_auto_2')
#cmo.setDirectory('/prj/obiee/CRPSTG/persistent_store/BipJmsStore')
exec conncmd2
cmo.setSynchronousWritePolicy('Direct-Write')
save()

cd('/FileStores/JRFWSAsyncFileStore_auto_1')
conncmd3="cmo.setDirectory('/prj/obiee/" + instName + "/persistent_store/JRFWSAsyncFileStore')"
#cmo.setDirectory('/prj/obiee/CRPSTG/persistent_store/JRFWSAsyncFileStore')
exec conncmd3
cmo.setSynchronousWritePolicy('Direct-Write')
save()

cd('/FileStores/JRFWSAsyncFileStore_auto_2')
#cmo.setDirectory('/prj/obiee/CRPSTG/persistent_store/JRFWSAsyncFileStore')
exec conncmd3
cmo.setSynchronousWritePolicy('Direct-Write')
save()

activate()
exit()
