from aiogram import Router, F
from aiogram.client.session import aiohttp
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.payload import decode_payload

from tgbot.config import Config
from tgbot.keyboards import reply_keyboards
from tgbot.misc import messages, states

router = Router(name='commands')


@router.message(CommandStart(deep_link=True))
async def command_start(message: Message, command: CommandObject, state: FSMContext):
    args = command.args
    await message.answer(
        'Это бот DonorSearch pet.\n\n'
        'Нажмите кнопку "Поделиться номером" чтобы подтвердить ваш номер телефона и привязать Telegram',
        reply_markup=reply_keyboards.phone_keyboard
    )
    await state.set_state(states.PhoneRequest.waiting_for_phone)
    await state.update_data(key=args)


@router.message(states.PhoneRequest.waiting_for_phone, F.content_type == ContentType.CONTACT)
async def link_telegram(message: Message, config: Config, state: FSMContext):
    if message.from_user.id != message.contact.user_id:
        await message.answer('Похоже это не ваш контакт...\n\nВоспользуйтесь кнопкой "Поделиться номер"',
                             reply_markup=reply_keyboards.phone_keyboard)
        return

    phone = message.contact.phone_number
    state_data = await state.get_data()
    key = state_data.get('key')

    url = (
        'http://89.223.30.75/api/telegram/link'
        f'?service_token={config.misc.service_api_token}&phone={phone}&key={key}&telegram_id={message.from_user.id}'
    )
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            if response.status != 204:
                await message.answer('Ой! Что-то пошло не так...',  reply_markup=ReplyKeyboardRemove())
                await state.clear()
                return

    await message.answer('Ура! Номер телефона подтверждён и Telegram привязан!', reply_markup=ReplyKeyboardRemove())
    await message.answer('Можете вернуться на сайт')

    await state.clear()


@router.message()
async def command_start(message: Message):
    await message.answer('Привет!\n\nЭто бот для DonorSearch Pet, используй его совместно с сайтом')
