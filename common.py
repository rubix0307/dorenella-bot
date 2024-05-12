import time

from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError
from asgiref.sync import sync_to_async

from ORM.models import User
from run import bot


async def send_admin_notification(notification_message: str) -> list:
    users_for_notification = await sync_to_async(list)(User.objects.filter(accepts_client_questions=True))
    user_ids = [ufn.id for ufn in users_for_notification]

    sent_messages = []
    for u_id in user_ids:
        try:
            sent_messages.append(await bot.send_message(u_id, notification_message))
        except TelegramForbiddenError as ex:
            continue

    return sent_messages


def update_user_info(message: Message) -> (User, bool):

    defaults = {
        'first_name': message.from_user.first_name,
        'full_name': message.from_user.full_name,
        'is_bot': message.from_user.is_bot,
        'is_premium': message.from_user.is_premium,
        'language_code': message.from_user.language_code,
        'last_name': message.from_user.last_name,
        'url': message.from_user.url,
        'username': message.from_user.username,

    }
    if message.contact:
        defaults.update({'phone_number': message.contact.phone_number})

    user, is_created = User.objects.update_or_create(id=message.from_user.id,
                                                            defaults=defaults,
                                                            create_defaults=defaults | {
                                                                'date_added': int(str(time.time())[:10])
                                                            }
                                                            )
    return user, is_created

async def aupdate_user_info(message: Message) -> (User, bool):
    return await sync_to_async(update_user_info)(message)