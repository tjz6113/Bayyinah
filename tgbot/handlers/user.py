from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


user_router = Router()

@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.forward(chat_id=6393999936,message_thread_id=message.message_thread_id, disable_notification=True)
    await message.reply("You are not allowed to use this bot")