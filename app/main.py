import asyncio
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types import InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from app.config import settings
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from app.config.db import init_db, add_client, init_roles, add_role, add_pending_request, init_pending_operators, remove_pending_request, approve_operator
from app.utils.validators import normalize_phone, validate_email, validate_name
from app.utils.rolemiddleware import RoleMiddleware
from app.services.operator_registration import process_operator_registration


dp = Dispatcher(storage=MemoryStorage())
router = Router()
role_middleware = RoleMiddleware()
router.message.middleware(role_middleware)
router.callback_query.middleware(role_middleware)
dp.include_router(router)

class AddClient(StatesGroup):
    waiting_for_name = State()
    waiting_for_email = State()
    waiting_for_phone = State()

@router.message(CommandStart())
async def cmd_welcome(message, role: str | None):
    if role is None:
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Зарегистрироваться", callback_data="start_register")]
        ])
        await message.answer("Добро пожаловать! Вы можете зарегистрироваться как оператор с помощью кнопки ниже.", reply_markup=keyboard)
    else:
        await message.answer(f"Добро пожаловать! Ваша роль: {role}. Вы можете добавить клиента с помощью команды /add_client_db.")

@router.message(Command("add_client_db"))
async def cmd_add_client_db(message, state: FSMContext, role: str | None):
    if role is None:
        await message.answer("Команда доступна только операторам.")
        return
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

@router.message(Command("whoami"))
async def whoami(message, role: str | None):
    if role:
        await message.answer(f"Ваша роль: {role}")
    else:
        await message.answer("У вас нет роли.")
        
@router.callback_query(F.data.startswith("approve_"))
async def approve_request(callback_query: types.CallbackQuery, bot: Bot):
    data = callback_query.data.split("_")
    user_id = int(data[1])
    role_name = data[2]
    await approve_operator(user_id, role_name)
    await bot.send_message(chat_id=user_id, text=f"Ваша роль была изменена на {role_name}.")
    await callback_query.message.edit_text(f"Запрос на роль оператора от пользователя {user_id} был одобрен и роль изменена на {role_name}.")
    await callback_query.answer("Запрос одобрен.")

@router.callback_query(F.data.startswith("reject_"))
async def reject_request(callback_query: types.CallbackQuery, bot: Bot):
    user_id = int(callback_query.data.split("_")[1])
    await remove_pending_request(user_id)
    await bot.send_message(chat_id=user_id, text="Ваш запрос на роль оператора был отклонен.")
    await callback_query.message.edit_text(f"Запрос на роль оператора от пользователя {user_id} был отклонен.")
    await callback_query.answer("Запрос отклонен.")


@router.callback_query(F.data == "start_register")
async def start_register(callback_query: types.CallbackQuery, role: str | None, bot: Bot):
    if role is not None:
        await callback_query.message.answer("Вы уже зарегистрированы как оператор.")
        await callback_query.answer()
        return
    response = await process_operator_registration(
        user_id=callback_query.from_user.id,
        username=callback_query.from_user.username,
        full_name=callback_query.from_user.full_name,
        bot=bot
    )
    await callback_query.message.answer(response)
    await callback_query.answer()

async def main():
    print("Application started")
    await init_db()
    await init_roles()
    await add_role(settings.ADMIN_ID, "admin")
    await init_pending_operators()
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

