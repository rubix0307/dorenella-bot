import time

from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from django.db.models.manager import Manager

from common import aupdate_user_info
from config import MenuKeyboard
from ORM.models import SystemText, User
from run import dp, router

@dp.message(CommandStart())
async def start(message: types.Message) -> None:
    message_user = message.from_user
    if not message_user.is_bot:
        await aupdate_user_info(message)

    caption = await SystemText.objects.aget(menu='start')
    photo = FSInputFile('media/start.jpg')
    await message.answer_photo(photo=photo, caption=caption.text.format_map(locals()), reply_markup=MenuKeyboard().get_start())

    try:
        await message.delete()
    except TelegramBadRequest:
        pass



@dp.message(Command(commands=['ban']))
async def user_ban(message: types.Message) -> None:
    user_objects: Manager = User.objects
    user = await user_objects.aget(id=message.from_user.id)

    if user and user.is_support:
        data = message.text.split(' ')
        if len(data) > 1:
            command, user_to_block_id, *_ = data

            try:
                user_to_block = await user_objects.aget(id=user_to_block_id)
                if user_to_block.is_banned:
                    user_to_block.is_banned = False
                    await user_to_block.asave()
                    await message.answer(text='Користувача розблоковано')
                else:
                    user_to_block.is_banned = True
                    await user_to_block.asave()
                    await message.answer(text='Користувача було заблоковано')

            except User.DoesNotExist:
                await message.answer(text='Користувач не знайдений')

        else:
            await message.answer(text='Вкажіть id користувача Telegram')
    else:
        await message.answer(text='Ви маєте бути адміністратором, для використання цієї команди')



