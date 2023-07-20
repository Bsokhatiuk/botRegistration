import qrcode as qrcode
from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN_API
from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import dao.modelDao as dao
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram_calendar.simple_calendar import calendar_callback as simple_cal_callback, SimpleCalendar
from aiogram_calendar.dialog_calendar import calendar_callback as dialog_cal_callback, DialogCalendar
import json

QR = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
# img = qrcode.make('https://t.me/Online_registration_bot')

# with open('qr.svg', 'wb') as qr:
#     img.save(qr)

bot = Bot(TOKEN_API)

dp = Dispatcher(bot)
# info = await bot.get_me()
# name = info.username

# @dp.message_handler()
# async def print(message:types.Message):
#     await message.answer(text=message.from_user.id)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton("⚒help")
b2 = KeyboardButton("start")
b3 = KeyboardButton("view", web_app=WebAppInfo(url="https://agile-tor-82473-26eff49ec440.herokuapp.com/stepform"))
b4 = KeyboardButton("qr")

kb.add(b1).insert(b2).add(b3).add(b4)

ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton("site", web_app=WebAppInfo(url="https://agile-tor-82473-26eff49ec440.herokuapp.com/stepform"))
ikb.add(ib1)
HELP_COMMENDS = """
<b>/start</b> - розпочати роботу бота
<b>⚒help</b> - список команд
"""


start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.row('Navigation Calendar', 'Dialog Calendar')


reply_requests = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Отправить свой контакт", request_contact=True))
reply_requests2 = InlineKeyboardMarkup().add(InlineKeyboardButton("Отправить свой контакт", request_contact=True))
async def on_startup(_):
    await dao.db_start_asc()

@dp.message_handler(text=['⚒help'])
async def help_command(message:types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=HELP_COMMENDS, parse_mode='HTML')
    await message.delete()

@dp.message_handler(commands=['start'])
async def start_command(message:types.Message):
    text = """ save user data """
    await dao.create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode='HTML',reply_markup=kb)


@dp.message_handler(commands=['contact'])
async def contact_command(message:types.Message):
    text = """ Відправити контакт? """
    await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode='HTML',reply_markup=reply_requests)
    # await message.delete()
@dp.message_handler(commands=['contact2'])
async def contact_command(message:types.Message):
    text = """ Відправити контакт? """
    await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode='HTML',reply_markup=reply_requests2)
    # await message.delete()
@dp.message_handler(content_types=['web_app_data'])
async def web_app_data_save(message:types.Message):
    res = json.loads(message.web_app_data.data)
    await message.answer(res)

@dp.message_handler(Text(equals=['qr'], ignore_case=True))
async def web_app_data_save(message:types.Message):
    # global QR
    QR.add_data("https://t.me/Online_registration_bot")
    QR.make(fit=True)
    img = QR.make_image(fill_color="black", back_color="white")
    img.save("qr.png")
    with open("qr.png", 'rb') as qrcode:
        await bot.send_photo(message.from_user.id, qrcode)
    QR.clear()

    # await bot.send_photo(chat_id=message.from_user.id, photo=img)


@dp.message_handler(Text(equals=['Navigation Calendar'], ignore_case=True))
async def nav_cal_handler(message: Message):
    await message.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())


# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d-%m-%Y")}',
            reply_markup=start_kb
        )


@dp.message_handler(Text(equals=['Dialog Calendar'], ignore_case=True))
async def simple_cal_handler(message: Message):
    await message.answer("Please select a date: ", reply_markup=await DialogCalendar().start_calendar())


# dialog calendar usage
@dp.callback_query_handler(dialog_cal_callback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d-%m-%Y")}',
            reply_markup=start_kb
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
