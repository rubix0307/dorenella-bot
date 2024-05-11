from typing import Any

from aiogram import F, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from asgiref.sync import sync_to_async
from django.db.models import Manager

from config import Action, MenuAction
from handlers.messages.common import send_admin_notification
from ORM.models import User, Question as UserQuestion
from run import bot, dp


class Question(StatesGroup):
    question = State()

def user_authorized(function):
    async def wrapper(callback_query, *args, **kwargs):
        user = await sync_to_async(list)(User.objects.filter(id=callback_query.message.chat.id))
        if user:
            user = user[0]
            if not user.is_banned:
                await function(callback_query, *args, **kwargs)
            else:
                await callback_query.answer('Ви не можете зробити цю дію')
    return wrapper



@dp.callback_query(MenuAction.filter(F.action == Action.ask_question.value))
@user_authorized
async def ask(callback_query: CallbackQuery, callback_data: MenuAction, state: FSMContext, *args, **kwargs):

    await state.set_state(Question.question)
    info_msg = await bot.send_message(chat_id=callback_query.message.chat.id,
        text='Напиши своє запитання\nДля скасування: /cancel',
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.update_data(info_msg_id=info_msg.message_id)
    await callback_query.answer()


@dp.message(Question.question and Command(commands=['cancel']))
async def cansel(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    info_msg_id = data.get('info_msg_id')
    if info_msg_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=info_msg_id)
    await message.delete()
    await state.clear()
    await message.answer('Скасовано',reply_markup=ReplyKeyboardRemove(),)

@dp.message(Question.question)
async def process_name(message: Message, state: FSMContext) -> None:

    msgs = (f'Користувач: {message.from_user.full_name} (#{message.from_user.id})',
            f'Питання:',
            f'',
            message.text,
            )
    notification_message = '\n'.join(msgs)
    # TODO

    sent_messages = await send_admin_notification(notification_message)

    if sent_messages:
        users_data = await sync_to_async(list)(User.objects.filter(id=message.from_user.id))
        if users_data:
            user = users_data[0]
            q = await UserQuestion.objects.acreate(text=message.text, user=user, type='question')
        await message.answer('Ваше запитання було надіслано')
    else:
        await message.answer('Ваше запитання не було надіслано')

    data = await state.get_data()
    info_msg_id = data.get('info_msg_id')
    if info_msg_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=info_msg_id)

    await state.clear()