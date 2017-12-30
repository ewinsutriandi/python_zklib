'''
Created on 2 Jul 2016

@author: ewien
'''
from ConfigParser import SafeConfigParser
import logging
import syncAttendance
import zklibs
import datetime
from zklibs import zklib

def prepareParams():
    parser = SafeConfigParser()
    parser.read('db.ini')
    global glIP,glDBuser,glDBpass, glDBschema,glLogFile
    glIP = parser.get('db', 'ip')
    glDBuser = parser.get('db', 'user')
    glDBpass = parser.get('db', 'password')
    glDBschema = parser.get('db', 'schema') 
    glLogFile = "synclog.txt"

class Device():
    
    def __init__(self,ip,port,devnum):
        self.ip = ip
        self.port = port
        self.devnum = devnum
        prepareParams()
        
    def synchronize(self):
        global glIP,glDBuser,glDBpass, glDBschema,glLogFile
        logging.basicConfig(filename=glLogFile,level=logging.INFO)
        zkdevice = zklib.ZKLib(self.ip,self.port)
        ret = zkdevice.connect()
        timeStart = datetime.datetime.now()
        logging.info(" start syncing machine with ID "+ str(self.devnum) + " @ "+ str(timeStart))
        
        if ret == True :
            logging.info(" Connected")
            
            data_user = zkdevice.getUser()
            logging.info (" Total user: %s" % (len(data_user)))
            
            attendance = zkdevice.getAttendance()
            logging.info (" Total scan: %s" % (len(attendance)))
            
            if ( attendance ):
                i = syncAttendance.Synchronizer(self.devnum)    
                for lattendance in attendance:
                    i.insert(lattendance)    
                logging.info(" Finished, " + str(i.databaru) +" record(s) synced")
       
            timeEnd = datetime.datetime.now()
            connectDuration = timeEnd - timeStart
            logging.info(" Duration : "+ str(connectDuration))
            zkdevice.disconnect()
        else:
            logging.info(" failed ")
     
        logging.info("_____________________END________________________")