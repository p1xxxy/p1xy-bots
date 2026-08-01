import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from app.config import settings
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from app.config.db import init_db, add_client, get_all_clients
from app.utils.validators import normalize_phone, validate_email, validate_name


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

@router.message(AddClient.waiting_for_name)
async def process_name(message, state: FSMContext):
    name = message.text
    valid_name = validate_name(name)
    if not valid_name:
        await message.answer("Некорректное имя. Попробуйте ещё раз.")
        return
    await state.update_data(name=valid_name)
    await message.answer("Какой у него email?")
    await state.set_state(AddClient.waiting_for_email)

@router.message(AddClient.waiting_for_email)
async def process_email(message, state: FSMContext):
    email = message.text
    normalized_email = validate_email(email)
    if not normalized_email:
        await message.answer("Некорректный email. Попробуйте ещё раз.")
        return
    await state.update_data(email=normalized_email)
    await message.answer("Какой у него телефон?")
    await state.set_state(AddClient.waiting_for_phone)

@router.message(AddClient.waiting_for_phone)
async def process_phone(message, state: FSMContext):
    phone = message.text
    normalized_phone = normalize_phone(phone)
    if not normalized_phone:
        await message.answer("Некорректный номер телефона. Попробуйте ещё раз.")
        return
    await state.update_data(phone=normalized_phone)
    data = await state.get_data()
    await add_client(
    name=data['name'],
    phone=data['phone'],
    email=data.get('email')
    )
    await message.answer("Клиент успешно добавлен!")
    await state.clear()


async def main():
    print("Application started")
    await init_db()
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

