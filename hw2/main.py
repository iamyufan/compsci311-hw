import asyncio
import socket

HOST = 'vcm-32603.vm.duke.edu'
PORT = 51300
ID = 'yz605'

connected_ports = []
secondary_connections = {}
listen_sockets = {}

async def handle_primary_connection(reader, writer):
    print("Connected to server on primary connection")
    writer.write(f"id {ID}\n".encode('ascii'))
    await writer.drain()

    data = await reader.readline()
    port = int(data.decode('ascii').strip().split()[1])

    try:
        secondary_task = asyncio.create_task(handle_secondary_connection(port, connected_ports))
        status_task = asyncio.create_task(handle_status_messages(reader))

        await asyncio.wait([secondary_task, status_task], return_when=asyncio.FIRST_COMPLETED)

        for task in [secondary_task, status_task]:
            if not task.done():
                task.cancel()
    except asyncio.CancelledError:
        writer.close()
        await writer.wait_closed()

    print(f"The connected ports are: {connected_ports}")


async def handle_secondary_connection(port, connected_ports):
    while True:
        if port in connected_ports:
            reader, writer = secondary_connections[port]
        else:
            reader, writer = await asyncio.open_connection(HOST, port)
            connected_ports.append(port)
            secondary_connections[port] = reader, writer

        print(f"Connected to server on secondary connection to port {port}")
        writer.write(f"id {ID}\n".encode('ascii'))
        await writer.drain()

        data = await reader.readline()
        if not data:
            writer.close()
            await writer.wait_closed()
            break

        message = data.decode('ascii').strip()
        print(f"Received message: {message}")
        if message.startswith('query'):
            new_port = int(message.split()[1])
            port = new_port
        elif message.startswith('listen'):
            listen_port = int(message.split()[1])
            listen_task = asyncio.create_task(handle_listen_message(listen_port))
        else:
            print(f"Unknown message received: {message}")


async def handle_listen_message(port):
    print(f"Listening for connections on port {port}")
    server = await asyncio.start_server(handle_client, port=port)
    async with server:
        await server.serve_forever()


async def handle_client(reader, writer):
    print("Connection established")
    writer.write(f"id {ID}\n".encode('ascii'))
    await writer.drain()

    while True:
        data = await reader.readline()
        if not data:
            break
        message = data.decode('ascii').strip()
        print(f"Received message: {message}")
        # Handle the message here
    writer.close()
    await writer.wait_closed()
    print("Connection closed")


async def handle_query_message(reader, writer):
    print(f"Received connection on listen port {writer.get_extra_info('peername')[1]}")
    writer.write(f"id {ID}\n".encode('ascii'))
    await writer.drain()

    while True:
        data = await reader.readline()
        if not data:
            break
        message = data.decode('ascii').strip()
        if message.startswith('query'):
            port = int(message.split()[1])
            if port in connected_ports:
                reader, writer = secondary_connections[port]
                writer.write(f"id {ID}\n".encode('ascii'))
                await writer.drain()


async def handle_status_messages(reader):
    while True:
        data = await reader.readline()
        if not data:
            break
        message = data.decode('ascii').strip()
        print(f"Received status message: {message}")
        for task in asyncio.all_tasks():
            task.cancel()


async def main():
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
        await handle_primary_connection(reader, writer)
    except (ConnectionRefusedError, socket.gaierror):
        print("Failed to connect to server")

if __name__ == '__main__':
    asyncio.run(main())
