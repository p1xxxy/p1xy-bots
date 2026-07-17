import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from app.config import settings

dp = Dispatcher()

async def main():
    print("Application started")
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

