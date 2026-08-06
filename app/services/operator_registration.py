from aiogram import Bot, types
from app.config import settings
from aiogram.types import InlineKeyboardButton
from app.config.db import add_pending_request

async def process_operator_registration(user_id: int, username: str | None, full_name: str, bot: Bot) -> str:
    """Обрабатывает команду /register для регистрации пользователя как оператора."""
    success = await add_pending_request(user_id, username, full_name)
    if success:
        username_display = f"@{username}" if username else "без username"
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Изменить роль на менеджера", callback_data=f"approve_{user_id}_manager")],
            [InlineKeyboardButton(text="Изменить роль на администратора", callback_data=f"approve_{user_id}_admin")],
            [InlineKeyboardButton(text="Отклонить", callback_data=f"reject_{user_id}")]
        ])
        await bot.send_message(chat_id=settings.ADMIN_ID, text=f"Новый запрос на роль оператора от {full_name} ({username_display}).", reply_markup=keyboard)
        return "Ваш запрос на роль оператора отправлен. Ожидайте подтверждения."
    else:
        return "Вы уже отправляли запрос на роль оператора. Пожалуйста, ожидайте подтверждения."
