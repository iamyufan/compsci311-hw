#!/usr/bin/env python3

import socket
import threading
from typing import Tuple

def read_line(r: socket.SocketType) -> str:
    sentinel = "\n".encode(encoding="ascii")
    buf = r.recv(1)
    while buf[-1] != sentinel[0]:
        buf += r.recv(1)
    line = buf.decode("ascii")
    return line


def handle_client(r: socket.SocketType, addr: Tuple):
    print(f"handling connection from {addr[0]}/{addr[1]}")
    r.settimeout(3.0)
    try:
        line = read_line(r)
    except TimeoutError:
        print("timeout: did not receive name within 3 seconds")
        r.close()
        return
    name = line.strip()
    print(f"connection by {name}")
    msg = f"hello {name}\n"
    r.send(msg.encode(encoding="ascii"))
    r.close()


PORT = 58200

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", PORT))
s.listen()
while True:
    (r, addr) = s.accept()
    t = threading.Thread(target=handle_client, args=(r, addr))
    t.daemon = True
    t.start()
