from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tgbot.misc import reply_commands


phone_keyboard = ReplyKeyboardBuilder()
phone_keyboard.button(text='Поделиться номером', request_contact=True)
phone_keyboard = phone_keyboard.as_markup(resize_keyboard=True)
