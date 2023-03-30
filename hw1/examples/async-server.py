#!/usr/bin/env python3

import asyncio
from asyncio import StreamReader, StreamWriter

PORT = 58200


async def handle_client(reader: StreamReader, writer: StreamWriter):
    try:
        buf = await asyncio.wait_for(reader.readline(), timeout=3.0)
    except TimeoutError:
        print("timeout: did not receive name within 3 seconds")
        writer.close()
        return
    name = buf.decode(encoding="ascii").strip()
    print(f"connection by {name}")
    msg = f"hello {name}\n"
    writer.write(msg.encode(encoding="ascii"))
    writer.close()


async def main():
    mainsrv = await asyncio.start_server(
        handle_client, host="0.0.0.0", port=PORT, reuse_address=True
    )
    task = asyncio.create_task(mainsrv.serve_forever())
    await task


if __name__ == "__main__":
    asyncio.run(main())
