#!/usr/bin/env python3

import asyncio

PORT = 58200


async def main():
    reader, writer = await asyncio.open_connection(host="localhost", port=PORT)
    writer.write("italo\n".encode(encoding="ascii"))
    buf = await reader.readline()
    line = buf.decode(encoding="ascii")
    msg = line.strip()
    print(f"received: {msg}")


if __name__ == "__main__":
    asyncio.run(main())
