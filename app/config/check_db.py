import asyncio
from app.config.db import get_all_clients

async def main():
    clients = await get_all_clients()
    for client in clients:
        print(client)

asyncio.run(main())