'''
Created on 31 Agt 2016

@author: STRUKTURAL01
'''
from ConfigParser import SafeConfigParser
import logging
global kocor

def init():
    parser = SafeConfigParser()
    parser.read('db.ini')
    global glIP,glDBuser,glDBpass, glDBschema,glLogFile,glLogging
    
    glIP = parser.get('db', 'ip')
    glDBuser = parser.get('db', 'user')
    glDBpass = parser.get('db', 'password')
    glDBschema = parser.get('db', 'schema') 
    glLogFile = "synclog.txt"
    glLogging = logging.basicConfig(filename=glLogFile,level=logging.INFO)