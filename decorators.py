from decouple import config
from aiogram import types

WHITELISTED_USERS = list(int(user_id) for user_id in config('WHITELISTED_USERS', default='', cast=str).split(','))

def whitelisted_users(handler):
    async def wrapper(message: types.Message):
        allowed_users = WHITELISTED_USERS
        if message.from_user.id not in allowed_users:
            return None
        return await handler(message)
    return wrapper
