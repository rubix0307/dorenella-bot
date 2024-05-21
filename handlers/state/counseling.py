from typing import Any

from aiogram import F, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hlink
from asgiref.sync import sync_to_async
from django.db.models import Manager

from common import aupdate_user_info, send_admin_notification, update_user_info
from config import Action, MenuAction, MenuKeyboard
from handlers.state.question import user_authorized
from ORM.models import User, Question as UserQuestion
from run import bot, dp



class OrderCounseling(StatesGroup):
    init_message = State()
    phone_number = State()
    instagram = State()


@dp.callback_query(MenuAction.filter(F.action == Action.counseling_message.value))
@user_authorized
async def ask(callback_query: CallbackQuery, callback_data: MenuAction, state: FSMContext, *args, **kwargs):

    await state.set_state(OrderCounseling.init_message)
    info_msg = await bot.send_message(chat_id=callback_query.message.chat.id,
        text='Чудово! Поділіться своєю проблемою та запитом, який ви хотіли б вирішити🩷\n\nДля скасування: /cancel',
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.update_data(info_msg_id=info_msg.message_id)
    await callback_query.answer()

@dp.message(OrderCounseling.init_message)
async def init_message(message: Message, state: FSMContext) -> None:

    await message.answer('Поділіться своїм контактом\n\nДля скасування: /cancel',
                         reply_markup=MenuKeyboard().get_share_contact())
    await state.update_data(init_message=message.text)
    await state.set_state(OrderCounseling.phone_number)



@dp.message(OrderCounseling.phone_number)
async def phone_number(message: Message, state: FSMContext) -> None:

    if message.contact:
        user, is_created = await aupdate_user_info(message)

        await message.answer('''Поділіться ім'ям користувача в інстаграм (для прикладу "@dorinellla"), якщо підтверджуєте замовлянння\n\nДля скасування: /cancel''',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(OrderCounseling.instagram)
    else:
        await message.answer('Ви маєте поділитися номером телефону саме за кнопкою нижче, якщо підтверджуєте замовлянння\n\nДля скасування: /cancel',
                             reply_markup=MenuKeyboard().get_share_contact())

@dp.message(OrderCounseling.instagram)
async def phone_number(message: Message, state: FSMContext) -> None:
    input_text = message.text

    if not '@' in input_text:
        await message.answer('''Ім'я користувача обов'язково має починатися з @''')
        return
    if len(input_text) < 3:
        await message.answer('''Ім'я користувача занадто коротке''')
        return

    if ' ' in input_text.strip():
        await message.answer('''Не вірне ім'я користувача''')
        return

    instagram_username = input_text.strip('@')

    user, is_created = await aupdate_user_info(message, instagram=instagram_username)
    data = await state.get_data()

    notification_message = [
        f'#консультація',
        data.get('init_message', '-'),
        f'',
        f'Користувач: {message.chat.full_name} ',
        f'@{message.chat.username} (#{message.chat.id})',
        f'''Телефон: {hlink(user.phone_number, url=f'http://t.me/{user.phone_number}')}''',
        f'''Instagram: {hlink(f'@{user.instagram}', url=f'https://www.instagram.com/{user.instagram}')}''',
    ]

    sent_messages = await send_admin_notification('\n'.join(notification_message))

    if sent_messages:
        await message.answer(text='Ваше замовлення консультації було відправлено',
                             reply_markup=ReplyKeyboardRemove(), )
        await UserQuestion.objects.acreate(text=data.get('init_message', '-'), user=user, type='consultation')
    else:
        await message.answer(text='Ваше замовлення консультації не було відправлено',
                             reply_markup=ReplyKeyboardRemove(), )

    data = await state.get_data()
    info_msg_id = data.get('info_msg_id')
    if info_msg_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=info_msg_id)
    await state.clear()
