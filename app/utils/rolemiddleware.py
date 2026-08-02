from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Any
from app.config.db import get_role

class RoleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id if event.from_user else None
        data['role'] = None
        if user_id is not None:
            role = await get_role(user_id)
            data['role'] = role
        return await handler(event, data)