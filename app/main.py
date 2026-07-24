import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from app.config import settings
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

class AddClient(StatesGroup):
    waiting_for_name = State()
    waiting_for_email = State()
    waiting_for_phone = State()

@router.message(CommandStart())
async def cmd_start_add_client(message, state: FSMContext):
    await message.answer("Как зовут вашего клиента?")
    await state.set_state(AddClient.waiting_for_name)
    

async def main():
    print("Application started")
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

