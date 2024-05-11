import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from dotenv import load_dotenv

import django
load_dotenv('.env')
django.setup()
from ORM.models import User

router = Router()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    from handlers import dp

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())