#!/usr/bin/env python3

import socket

PORT = 58200

def read_line(r: socket.SocketType) -> str:
    sentinel = "\n".encode(encoding="ascii")
    buf = r.recv(1)
    while buf[-1] != sentinel[0]:
        buf += r.recv(1)
    line = buf.decode("ascii")
    return line

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", PORT))

s.send("italo\n".encode(encoding="ascii"))
line = read_line(s)
msg = line.strip()
print(f"received: {msg}")
