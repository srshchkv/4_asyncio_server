import asyncio

async def scan_port(host, port, sem):
    async with sem:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            print(f"Port {port} is open")
            writer.close()
            await writer.wait_closed()
        except OSError:
            pass

async def scan_ports(host, ports):
    sem = asyncio.Semaphore(1000)  # Limit concurrent connections
    tasks = [scan_port(host, port, sem) for port in ports]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    host = input("Enter the hostname or IP address: ")
    ports = range(1, 1025)  # Scan common ports
    asyncio.run(scan_ports(host, ports))
