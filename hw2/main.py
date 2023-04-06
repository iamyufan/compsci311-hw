import asyncio

HOST = 'vcm-32603.vm.duke.edu'
PORT = 51300
ID = 'yz605'

SEC_PORTS = []
SEC_CONN = {}
LISTEN_PORTS = []
LISTEN_SERVERS = {}


def write_id_message(writer):
    '''
    Write the ID message to the server
    '''
    writer.write(f"id {ID}\n".encode('ascii'))


async def handle_listen_connection(reader, writer):
    '''
    Handle the listen connection from the server
    '''
    print(f"> Listening on port {writer.get_extra_info('sockname')[1]}: server established")
    # Handle the received message
    while True:
        data = await reader.readline()
        if not data:
            break

        message = data.decode('ascii').strip()
        print(f"> Listening on port {writer.get_extra_info('sockname')[1]}: received message {message}")
        query_port = int(message.split()[1])
        asyncio.create_task(handle_secondary_connection(query_port))


async def handle_status_messages(reader):
    '''
    Handle the status message from the server
        - SUCCESS = "success"
        - ID_READ_TIMEOUT = "timeout while reading identification message"
        - ID_PARSE_ERROR = "failed to parse identification message"
        - ID_WITHOUT_SESSION = "secondary connection but no active session"
        - CONCURRENT_SESSION = "primary connection but existing active session"
        - ID_FROM_DIFF_HOST = "identification from different remote host"
        - DUPLICATE_SECONDARY = "duplicate secondary connection"
        - UNEXPECTED_ID = "unexpected id message"
        - INVALID_ID = "invalid identifier in id message"
        - CONNECTION_FAILURE = "failure to connect to a remote port"
    '''
    while True:
        # Wait for a status message from the server
        data = await reader.readline()
        if not data:
            break
            
        # Print the message and cancel all other coroutines
        message = data.decode('ascii').strip()
        print(f"Received status message: {message}")
        for task in asyncio.all_tasks():
            task.cancel()
        for s in LISTEN_SERVERS.values():
            s.close()


async def create_server(port):
    '''
    Create a new server for the listen message
    '''
    server = await asyncio.start_server(handle_listen_connection, port=port)
    LISTEN_SERVERS[port] = server
    async with server:
        await server.serve_forever()


async def handle_listen_server(listen_port):
    '''
    Handle the listen message from the server
    '''
    LISTEN_PORTS.append(listen_port)
    asyncio.create_task(create_server(listen_port))


async def handle_secondary_connection(port):
    '''
    Handle the secondary connection to the server
    - Receive the query message and open a new connection
    - Receive the listen message and open a new server
    '''
    # If the port is already visited, simply write the ID message
    if port in SEC_PORTS:
        reader, writer = SEC_CONN[port]
        print(f"Connected to server on secondary connection to port {port} (visited)")
        # Write the ID message
        write_id_message(writer)
    # If the port is never visited, open a new connection and handle the message
    else:
        reader, writer = await asyncio.open_connection(HOST, port)
        SEC_PORTS.append(port)
        SEC_CONN[port] = reader, writer
        print(f"Connected to server on secondary connection to port {port}")

        # Write the ID message
        write_id_message(writer)

        # Handle the received message
        while True:
            # Wait for a message from the server
            data = await reader.readline()
            if not data:
                break

            msg = data.decode('ascii').strip()
            msg_type = msg.split()[0]
            msg_port = int(msg.split()[1])

            # Handle query message
            if msg_type == "query":
                asyncio.create_task(handle_secondary_connection(msg_port))
            
            # Handle listen message
            elif msg_type == "listen":
                asyncio.create_task(handle_listen_server(msg_port)) 


async def handle_primary_connection():
    '''
    Handle the primary connection to the server
        - Receive the first port for secondary connection
        - Receive the status message and close all the connection
    '''
    # Open connection to the primary port
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print("Connected to server on primary connection")

    # Write the ID message
    write_id_message(writer)

    # Receive the first port for secondary connection
    data = await reader.readline()
    new_port = int(data.decode('ascii').strip().split()[1])

    try:
        # Establish the first secondary connection
        await asyncio.create_task(handle_secondary_connection(new_port))
        # Listen and handle the status message
        await asyncio.create_task(handle_status_messages(reader))
    except asyncio.CancelledError:
        # If one of the coroutines is cancelled, close the writer and wait for it to be closed
        writer.close()
        await writer.wait_closed()


async def main():
    await handle_primary_connection()
    print(f"The connected ports are: {SEC_PORTS}")
    print(f"The listening ports are: {LISTEN_PORTS}")


if __name__ == '__main__':
    asyncio.run(main())
