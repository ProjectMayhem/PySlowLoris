"""This module contains helper functions."""

def try_detect_webserver(target):
    """Tries to detect the host's webserver."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.connect((target.host, target.port))
        sock.send("GET / HTTP/1.1\r\n\r\n".encode("ascii"))
        response = sock.recv(1024).decode("utf-8")
        sock.shutdown(1)
        sock.close()
    except: # pylint: disable=bare-except
        return None
    for line in response.split("\r\n"):
        if line.startswith("Server:"):
            return line.split("Server:")[1].strip()
    return None
