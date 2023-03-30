# Yufan Zhang (NetID: yz605)
# CompSci 311 (SP23) Assignment 1

import asyncio
import socket

HOST = 'vcm-32603.vm.duke.edu'
PORT = 51200
ID = 'yz605'

connected_ports = []        # records the ports that have been connected
secondary_connections = {}  # dictionary that stores the secondary connections, with the port number as keys


# Handles the primary connection to the server
async def handle_primary_connection(reader, writer):
    print("Connected to server on primary connection")

    # Send the ID to the server at the very beginning
    writer.write(f"id {ID}\n".encode('ascii'))
    await writer.drain()

    # Wait for the server to send the first port number
    data = await reader.readline()
    port = int(data.decode('ascii').strip().split()[1])

    try:
        # Start two coroutines in parallel: handle_secondary_connection and handle_status_messages
        await asyncio.gather(handle_secondary_connection(port, connected_ports), handle_status_messages(reader))
    except asyncio.CancelledError:
        # If one of the coroutines is cancelled, close the writer and wait for it to be closed
        writer.close()
        await writer.wait_closed()

    # Print the list of connected ports
    print(f"The connected ports are: {connected_ports}")


# Handles the secondary connection to the server
async def handle_secondary_connection(port, connected_ports):
    while True:
        if port in connected_ports:
            # If the port is already connected, get the existing reader and writer objects
            reader, writer = secondary_connections[port]
        else:
            # If the port is not already connected, open a new connection
            reader, writer = await asyncio.open_connection(HOST, port)
            connected_ports.append(port)
            secondary_connections[port] = reader, writer

        # Send the ID to the server
        print(f"Connected to server on secondary connection to port {port}")
        writer.write(f"id {ID}\n".encode('ascii'))
        await writer.drain()

        # Wait for the server to send a new port number
        data = await reader.readline()
        if not data:
            # If there is no data, close the writer and wait for it to be closed
            writer.close()
            await writer.wait_closed()
            break

        # Extract the new port number and update the loop variable
        new_port = int(data.decode('ascii').strip().split()[1])
        port = new_port


# # Handles status messages from the server
async def handle_status_messages(reader):
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


async def main():
    try:
        # Open the initial connection to the server
        reader, writer = await asyncio.open_connection(HOST, PORT)
        await handle_primary_connection(reader, writer)
    except (ConnectionRefusedError, socket.gaierror):
        print("Failed to connect to server")


if __name__ == '__main__':
    asyncio.run(main())
