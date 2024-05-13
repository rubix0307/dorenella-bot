from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hlink
from asgiref.sync import sync_to_async

from common import aupdate_user_info, send_admin_notification
from config import Action, MenuAction, MenuKeyboard
from ORM.models import Question as UserQuestion, User
from run import bot, dp


class Question(StatesGroup):
    question = State()
    phone_number = State()

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


@dp.message(Question.question and Command(commands=['cancel']))
async def cansel(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    info_msg_id = data.get('info_msg_id')
    if info_msg_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=info_msg_id)

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    await state.clear()
    await message.answer('Скасовано',reply_markup=ReplyKeyboardRemove(),)

@dp.callback_query(MenuAction.filter(F.action == Action.ask_question.value))
@user_authorized
async def ask(callback_query: CallbackQuery, callback_data: MenuAction, state: FSMContext, *args, **kwargs):

    await state.set_state(Question.question)

    text = '\n'.join([
        f'Тут ви можете вказати додаткові питання, якщо вони виникли, щодо особистої роботи або форматів☺️',
        f'',
        f'Кожна людина індивідуальна та потребує унікального підходу, тож моя задача забезпечити вас цим🩷',
        f'',
        f'Для скасування: /cancel',
    ])

    info_msg = await bot.send_message(chat_id=callback_query.message.chat.id,
        text=text,
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.update_data(info_msg_id=info_msg.message_id)
    await callback_query.answer()




@dp.message(Question.question)
async def process_name(message: Message, state: FSMContext) -> None:
    await message.answer('Поділіться своїм контактом, якщо підтверджуєте надсилання запитання\n\nДля скасування: /cancel',
                         reply_markup=MenuKeyboard().get_share_contact())
    await state.update_data(init_message=message.text)
    await state.set_state(Question.phone_number)


@dp.message(Question.phone_number)
async def phone_number(message: Message, state: FSMContext) -> None:

    if message.contact:
        user, is_created = await aupdate_user_info(message)
        data = await state.get_data()

        clean_phone_number = '+' + message.contact.phone_number.replace("+", "")
        notification_message = [
            f'#питання',
            data.get('init_message', '-'),
            f'',
            f'Користувач: {message.chat.full_name} ',
            f'@{message.chat.username} (#{message.chat.id})',
            f'''Телефон: {hlink(clean_phone_number, url=f'http://t.me/{clean_phone_number}')}''',
        ]

        sent_messages = await send_admin_notification('\n'.join(notification_message))

        if sent_messages:
            q = await UserQuestion.objects.acreate(text=data.get('init_message', '-'), user=user, type='question')
            await message.answer('Ваше запитання було надіслано', reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer('Ваше запитання не було надіслано', reply_markup=ReplyKeyboardRemove())

        data = await state.get_data()
        info_msg_id = data.get('info_msg_id')
        if info_msg_id:
            await bot.delete_message(chat_id=message.chat.id, message_id=info_msg_id)

        await state.clear()
    else:
        await message.answer('Ви маєте поділитися номером телефону саме за кнопкою нижче, якщо підтверджуєте замовлянння\n\nДля скасування: /cancel',
                             reply_markup=MenuKeyboard().get_share_contact())

