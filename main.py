from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN_API
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import dao.modelDao as dao
bot = Bot(TOKEN_API)

dp = Dispatcher(bot)

# @dp.message_handler()
# async def print(message:types.Message):
#     await message.answer(text=message.from_user.id)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton("⚒help")
b2 = KeyboardButton("start")
b3 = KeyboardButton("view", web_app=WebAppInfo(url="https://telemetr.io/uk/channels"))

kb.add(b1).insert(b2).add(b3)

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton
HELP_COMMENDS = """
<b>/start</b> - розпочати роботу бота
<b>⚒help</b> - список команд
"""

async def on_startup(_):
    await dao.db_start()

@dp.message_handler(text=['⚒help'])
async def help_command(message:types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=HELP_COMMENDS, parse_mode='HTML')
    await message.delete()

@dp.message_handler(commands=['start'])
async def start_command(message:types.Message):
    text = """ save user data """
    await dao.create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode='HTML',reply_markup=kb)
    # await message.delete()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
