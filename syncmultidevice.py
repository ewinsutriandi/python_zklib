'''
Created on 5 Mei 2016

@author: ewien
'''

from ConfigParser import SafeConfigParser
import MySQLdb
import logging
import device


def prepareParams():
    parser = SafeConfigParser()
    parser.read('db.ini')
    global glIP,glDBuser,glDBpass, glDBschema,glLogFile
    glIP = parser.get('db', 'ip')
    glDBuser = parser.get('db', 'user')
    glDBpass = parser.get('db', 'password')
    glDBschema = parser.get('db', 'schema') 
    glLogFile = "synclog.txt"

def syncDevice():
    logging.basicConfig(filename=glLogFile,level=logging.INFO)
    logging.info(" loading devices ")
    db = MySQLdb.connect(glIP,glDBuser,glDBpass,glDBschema)
    cursor = db.cursor()
    sql = "SELECT ip,port,id FROM mesin"
    try :
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            ip = row[0]
            port = row[1]
            devnum = row[2]
            dev = device.Device(ip,port,devnum)
            dev.synchronize()
    except Exception,e:
        print str(e)
        logging.info(" Can't create connection ")
    db.close()

prepareParams()
syncDevice()