import asyncio

async def handle_client(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode().strip()
        if not message:
            break

        if message == "/shutdown":
            print("Server shutting down...")
            writer.write("Server shutting down...".encode())
            await writer.drain()
            asyncio.get_event_loop().stop()
        else:
            response = f"Received: {message}"
            writer.write(response.encode())
            await writer.drain()

    writer.close()

async def main(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    host = 'localhost'
    port = 9095
    asyncio.run(main(host, port))
