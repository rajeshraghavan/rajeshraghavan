##################################################################################################
#This scripts extracts he parameter from a text file and creates the Application roles in FMW and adds the qgroup with the same name to it.
#Author - rajeshr
#Questions - mwss.bi.team@qualcomm.com
#Date - 05/14/2014
#Usage - $mw_home/oracle_common/common/bin/wlst.sh Create_grant_role_em_bu.py host_name port_no weblogic password buname
#This scripts will need the text files crp_AppRoles.txt, crp_BIAuthor.txt and crp_BIAdmin.txt
##################################################################################################

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
       
#################
#Main
#################

#connect('weblogic','obipoc11g1','obi117poc1:7001')

wlshostname=sys.argv[1]
wlsport=sys.argv[2]
wlsusrname=sys.argv[3]
wlspassword=sys.argv[4]
buname=sys.argv[5]


connectwls(wlsusrname,wlspassword,wlshostname,wlsport)

appStripe='obi'

#AppRoles = open("QMART_AppRoles.txt")
apprcmd1="AppRoles=open('" + buname + "_AppRoles.txt')"
print apprcmd1
exec apprcmd1
#AppRoles = open("crp_AppRoles.txt")
for approle in AppRoles:
    approle = approle.rstrip()
    print str(datetime.now()) + ': Creating the AppRole ' + approle
    try:
       createAppRole(appStripe=appStripe, appRoleName=approle)
    except:
       print str(datetime.now()) + ': Could not create the Application Role ' + approle
#      AppRoles.close()
#      sys.exit()
       continue      
    print str(datetime.now()) + ': Adding the qgroup ' + approle + ' to the AppRole ' + approle
    try:
       grantAppRole(appStripe=appStripe, appRoleName=approle, principalClass='weblogic.security.principal.WLSGroupImpl', principalName=approle)
    except:
       print str(datetime.now()) + ': The qgroup ' + approle + ' could not be added to the Application role ' + approle
#      AppRoles.close()
#      sys.exit()
       continue
AppRoles.close()

#AppRoles1 = open("QMART_BIAuthor.txt")
#AppRoles1 = open("crp_BIAuthor.txt")
apprcmd2="AppRoles1=open('" + buname + "_BIAuthor.txt')"
exec apprcmd2

for approle1 in AppRoles1:
	approle1 = approle1.rstrip()
	print str(datetime.now()) + ': Adding the AppRole ' + approle1 + ' to BIAuthor role.'
	try:
            cmd1="grantAppRole(appStripe=appStripe, appRoleName='BIAuthor', principalClass='oracle.security.jps.service.policystore.ApplicationRole', principalName='" + approle1 + "')"
	    exec cmd1
        except:
            continue

#grantAppRole(appStripe=appStripe, appRoleName='BIAuthor', principalClass='oracle.security.jps.service.policystore.ApplicationRole', principalName='OBIEE_CORPFIN_FUNC_REV_ADMIN')

#AppRoles2 = open("QMART_BIAdmin.txt")            
#AppRoles2 = open("crp_BIAdmin.txt")
apprcmd3="AppRoles2=open('" + buname + "_BIAdmin.txt')"
exec apprcmd3
for approle2 in AppRoles2:
	approle2 = approle2.rstrip()
	print str(datetime.now()) + ': Adding the AppRole ' + approle2 + ' to BIAuthor role.'
	try:
            cmd2="grantAppRole(appStripe=appStripe, appRoleName='BIAdministrator', principalClass='oracle.security.jps.service.policystore.ApplicationRole', principalName='" + approle2 + "')"
            exec cmd2
        except:
            continue

#grantAppRole(appStripe=appStripe, appRoleName='BIAdministrator', principalClass='oracle.security.jps.service.policystore.ApplicationRole', principalName='OBIEE_ERP_ADMIN')
