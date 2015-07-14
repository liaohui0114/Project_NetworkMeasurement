import os
from PassiveClient import *
from time import *

if __name__ == '__main__':
    try:
        if os.fork() > 0:
            os._exit(0)
    except OSError, error:
        print 'error'
        os._exit(1)
        
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            print 'Daemon PID %d' %pid
            os._exit(0)
    except OSError, error:
        print 'error'
        os._exit(1)
    
    while True:
        passiveClient()
        sleep(1800)
        