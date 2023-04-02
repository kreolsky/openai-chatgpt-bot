import logging
from decouple import config
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from storage import RedisConnection, UserManager
from decorators import whitelisted_users
from handlers import help_handler, reset_handler, userid_handler, start_handler, message_handler

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot, dispatcher, and Redis
bot = Bot(token=config('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

redis_conn = RedisConnection(config('REDIS_URL'))
user_manager = UserManager(redis_conn)

@dp.message_handler(commands=['help'])
@whitelisted_users
async def help_command(message: types.Message):
    await help_handler(message, bot)

@dp.message_handler(commands=['reset'])
@whitelisted_users
async def reset_command(message: types.Message):
    await reset_handler(message, bot, user_manager)

@dp.message_handler(commands=['userid'])
async def userid_command(message: types.Message):
    await userid_handler(message, bot)

@dp.message_handler(commands=['start'])
@whitelisted_users
async def start_command(message: types.Message):
    await start_handler(message, bot)

@dp.message_handler(content_types=types.ContentTypes.TEXT)
@whitelisted_users
async def process_message(message: types.Message):
    await message_handler(message, bot, user_manager)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
