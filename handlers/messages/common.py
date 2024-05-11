from asgiref.sync import sync_to_async
from ORM.models import User
from run import bot


async def send_admin_notification(notification_message: str) -> list:
    users_for_notification = await sync_to_async(list)(User.objects.filter(accepts_client_questions=True))
    user_ids = [ufn.id for ufn in users_for_notification]

    sent_messages = []
    for u_id in user_ids:
        sent_messages.append(await bot.send_message(u_id, notification_message))

    return sent_messages


def chunk_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]