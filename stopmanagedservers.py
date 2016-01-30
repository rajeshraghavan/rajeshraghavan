###########################################################################################
#This scripts stops all the Managed Servers in a Weblogic domain
#Author - rajeshr
#Questions - mwss.bi.team@qualcomm.com
#Usage - java weblogic.WLST stopmanagedservers.py Admin_Server_Name Admin_Port Admin_UserName Admin_Password
#Date - 10/17/2012
###########################################################################################


def connectwls(wlsusername,wlspassword,wlshostname,wlsport):
    try:
        conncmd1="connect('" + wlsusrname + "', '" + wlspassword + "', '" + wlshostname + ":" + wlsport + "')"
        exec conncmd1
    except:
        print "Couldn't connect to the WLS admin server, verify if the " + wlshostname + ":" + wlsport + " is accessible."     

#    WLS_URL=wlshostname + ":" + wlsport
    
def server_state(svrName):
    sstate = 'UNKNOWN'
    try :
        myTree = currentTree()
        domainRuntime()
        #cd( '/ServerLifeCycleRuntimes/' + svrName.getName())
        #sstate = cmo.getState()
#       print svrName 
        sstate = cmo.lookupServerLifeCycleRuntime(svrName).getState()
#       print sstate
        myTree()
    except:
        print 'Exception while trying to get ServerRuntimeMBean'
        dumpStack()
        myTree()
    return sstate

def stopManagedServers():
#    connectwls()
    srvs = cmo.getServers()
    for server in srvs:
        svrStatus = server_state(server.getName())
        ntries = 0
        if server.getName() != 'AdminServer':
           svrStatus = server_state(server.getName())
           print server.getName() + " is " + svrStatus + " state"
           if svrStatus == "RUNNING":
              print "Stopping server " + server.getName() + " : " +  str(datetime.now())
              shutdown(server.getName(),'Server', ignoreSessions='true', force='true')
              PyTime.sleep(10)
              while (ntries < 3):
                   ntries = ntries+1
                   PyTime.sleep(10)
                   svrStatus = server_state(server.getName())
                   if svrStatus == "SHUTDOWN":
                      print "Managed Server " + server.getName() + " is in the STOPPED state now" + " : " +  str(datetime.now())
                      break
           svrStatus = server_state(server.getName())
        elif svrStatus == "SHUTDOWN":
           print "Managed Server " + server.getName() + " is already stopped" 
       
        elif (ntries == 3 and svrStatus != 'SHUTDOWN'):
           print "Managed Server " + svrName + " is stopping now" + " : " +  str(datetime.now())

        else:
           print "Stopping Managed Server"

###############################################
#Main
###############################################

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

#wlsport=raw_input('Enter the Weblogic Admin Server Port Number: ')
#str_nm=raw_input('Do you want NodeManager to be restarted - Type yes or no: ')
WLS_URL=wlshostname + ":" + wlsport

connectwls(wlsusrname,wlspassword,wlshostname,wlsport)
stopManagedServers()
