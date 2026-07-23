import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import Router
from aiogram.filters import CommandStart
from app.config import settings
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.state import State
from aiogram.fsm.storage.memory import MemoryStorage


dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

class AddClient(StatesGroup):
    waiting_for_name = State()
    waiting_for_email = State()
    waiting_for_phone = State()

@router.message(CommandStart())
async def command_start_handler(message):
    await message.answer("Hello, world!")
    

async def main():
    print("Application started")
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

