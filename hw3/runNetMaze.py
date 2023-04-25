import json
import socket
import threading

HOST = 'vcm-32603.vm.duke.edu'
PORT = 51300
ID = "yz605"

lock = threading.Lock()
SOCKETS = {}
THREADS = {}
CONNECTIONS = {}
executing = True


def handle_listen(port, query_list):
    s_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_listen.bind(("0.0.0.0", port))
    s_listen.listen()
    s_listen.settimeout(None)
    (r_listen, addr_listen) = s_listen.accept()
    CONNECTIONS[port] = "server"

    while executing:
        line = read_line(r_listen)
        handle_msg(line, query_list, port)


def read_line(r):
    sentinel = "\n".encode(encoding="ascii")
    buf = r.recv(1)
    if not buf:
        return ""
    while buf[-1] != sentinel[0]:
        buf += r.recv(1)
    line = buf.decode("ascii")
    return line


def handle_port(port, query_list):
    r = SOCKETS[port]
    while executing:
        line = read_line(r)
        handle_msg(line, query_list, port)


def handle_msg(line, query_list, self_port):
    if (line == ""):
        global executing
        executing = False
        return

    msg = line.strip().split(" ", 1)
    msg_type = msg[0]

    # Handle query message
    if msg_type == "query":
        curr_port = int(msg[1])
        lock.acquire()  # prevent duplicate secondary connections
        # If the port is already visited, simply write the ID message
        if (curr_port in SOCKETS):
            SOCKETS[curr_port].send(f"id {ID}\n".encode(encoding="ascii"))

        # If the port is never visited, open a new connection and handle the message
        else:
            curr_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            curr_s.settimeout(None)
            curr_s.connect((HOST, curr_port))
            SOCKETS[curr_port] = curr_s
            CONNECTIONS[curr_port] = "client"
            curr_s.send(f"id {ID}\n".encode(encoding="ascii"))
            THREADS[curr_port] = threading.Thread(
                target=handle_port, args=(curr_port, query_list))
            THREADS[curr_port].daemon = True
            THREADS[curr_port].start()

        # Store the query info into the query_list
        query_info = {
            "connection_source": CONNECTIONS[self_port],
            "connection_port": self_port,
            "query_target": curr_port
        }
        query_list.append(json.dumps(query_info))

        lock.release()  # release lock
        return

    # Handle listen message
    elif msg_type == "listen":
        # print("trying listening")
        curr_port = int(msg[1])
        THREADS[curr_port] = threading.Thread(
            target=handle_listen, args=(curr_port, query_list, ))
        THREADS[curr_port].daemon = True
        THREADS[curr_port].start()
        return

    # Handle status message
    elif msg_type == "status":
        for port in SOCKETS:
            SOCKETS[port].close
        executing = False
        return


def get_query_list(input_id):
    global ID, SOCKETS, THREADS, CONNECTIONS, executing
    ID = input_id
    SOCKETS = {}
    THREADS = {}
    CONNECTIONS = {}
    executing = True

    # initialize primary socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(None)
    s.connect((HOST, PORT))
    SOCKETS[PORT] = s
    CONNECTIONS[PORT] = "client"
    s.send(f"id {ID}\n".encode(encoding="ascii"))

    query_list = []

    while (executing):
        line = read_line(s)
        handle_msg(line, query_list, PORT)

    return query_list
