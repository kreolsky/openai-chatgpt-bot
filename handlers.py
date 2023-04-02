from storage import UserManager
from aiogram import types, Bot
from decouple import config
import openai
import requests
import json

# Set up OpenAI API key
openai.api_key = config('OPENAI_API_KEY')

async def help_handler(message: types.Message, bot):
    help_text = (
        "/start - Welcome message and instructions\n"
        "/help - List available commands\n"
        "/reset - Clear user history\n"
        "/userid - Return your Telegram ID\n"
    )
    await bot.send_message(chat_id=message.chat.id, text=help_text)

async def reset_handler(message: types.Message, bot, user_manager: UserManager):
    user_manager.clear_history(user_id=message.from_user.id)
    await bot.send_message(chat_id=message.chat.id, text="User history cleared.")

async def userid_handler(message: types.Message, bot):
    await bot.send_message(chat_id=message.chat.id, text=f"Your Telegram ID: {message.from_user.id}")

async def start_handler(message: types.Message, bot):
    start_text = (
        "Welcome to the GPT-4 Chatbot!\n"
        "Just type your message and the bot will respond. Use /help for more commands."
    )
    await bot.send_message(chat_id=message.chat.id, text=start_text)

def convert_history_to_messages(history):
    messages = []
    for message in history:
        messages.append({"role": message["role"], "content": message["text"]})
    return messages

async def message_handler(message: types.Message, bot: Bot, user_manager: UserManager):
    if message.text.startswith('/'):
        return

    user_id = message.from_user.id
    user_manager.add_message(user_id=user_id, role='user', text=message.text)

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    history = user_manager.get_history(user_id)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=convert_history_to_messages(history),
        max_tokens=300,
        temperature=0.9,
    )

    # Extract the response text from the API response
    response_text = response.choices[0]['message']['content'].strip()

    user_manager.add_message(user_id=user_id, role='assistant', text=response_text)
    await bot.send_message(chat_id=message.chat.id, text=response_text)
