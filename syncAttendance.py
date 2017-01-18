'''
Created on 3 Mei 2016

@author: ewien
'''
from ConfigParser import SafeConfigParser
import MySQLdb
import logging

def prepareParams():
    parser = SafeConfigParser()
    parser.read('db.ini')
    global glIP,glDBuser,glDBpass, glDBschema,glLogFile
    glIP = parser.get('db', 'ip')
    glDBuser = parser.get('db', 'user')
    glDBpass = parser.get('db', 'password')
    glDBschema = parser.get('db', 'schema') 
    glLogFile = "synclog.txt"

class Synchronizer():
    '''
    class to insert attendance data to database
    '''

    def __init__(self,devnum):
        '''
        Constructor
        '''
        prepareParams()
        global glIP,glDBuser,glDBpass, glDBschema,glLogFile
        logging.basicConfig(filename=glLogFile,level=logging.INFO)
        self.db = MySQLdb.connect(glIP,glDBuser,glDBpass,glDBschema)
        def userLastScanTime(self):
            sql = """select max(scantime) from attlog"""
            c = self.db.cursor()
            try:
                c.execute(sql)
                result = c.fetchall()
                if (result):
                    row = result [0]
                    return row[0]
                else:
                    return None
                
            except MySQLdb.Error as e:
                print e
                logging.error(str(e))
            finally:
                c.close()
        self.maxscantime = userLastScanTime(self)
        self.databaru = 0
        self.devnum = devnum
        #print "max scan time : %s" % (self.maxscantime) 
        logging.info(" Scan terakhir sebelum sync :"+ str(self.maxscantime))
    
    def insert(self, attendanceRecord):
        
        uid = attendanceRecord[0]
        scantime = attendanceRecord[2]
        b = True
        if (self.maxscantime != None):
            if (self.maxscantime >= scantime):
                b = False
        
        if (b):
            self.databaru += 1
            print "uid scan time : %s %s" % (uid,scantime)  
            sql = """INSERT INTO attlog(uid,scanTime,mesin_id)
                VALUES (%s, %s, %s)"""
            
            
            c = self.db.cursor()
            
            try:
                c.execute(sql,(uid,scantime,str(self.devnum)))
                self.db.commit() 
                
            except MySQLdb.Error as e:
                #c.rollback()
                print e
    
            finally: 
                c.close()    
            
    
   
        
        