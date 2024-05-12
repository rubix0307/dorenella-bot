import copy
from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder


class Action(Enum):
    open_menu = 'open'
    ask_question = 'ask_question'
    accompaniment_message = 'accompaniment_message'
    counseling_message = 'counseling_message'

class MenuName(Enum):
    trust = 'trust'
    trust_back = 'trust_back'
    services = 'services'
    test = 'test'
    counseling = 'counseling'
    accompaniment = 'accompaniment'
    accompaniment_back = 'accompaniment_back'
    feedbacks = 'feedbacks'
    feedbacks_back = 'feedbacks_back'
    start = 'start'
    order_counseling = 'order_counseling'
    order_accompaniment = 'order_accompaniment'
    accompaniment_detail = 'accompaniment_detail'
    todo = 'TODO'

class MenuAction(CallbackData, prefix='menu'):
    action: str
    menu: str | None = None
    page: int | None = None

class MenuButton(Enum):
    trust = InlineKeyboardButton(text=f"Чому мені можна довіряти? ",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.trust.value).pack(),
        )
    trust_back = InlineKeyboardButton(text=f"Назад",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.trust_back.value).pack(),
        )
    services = InlineKeyboardButton(text=f"Послуги",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.services.value).pack(),
        )
    ask_me = InlineKeyboardButton(text=f"Задати питання",
        callback_data=MenuAction(
            action=Action.ask_question.value).pack(),
        )
    test = InlineKeyboardButton(text=f"Пройти тест",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.test.value).pack(),
        )
    test_url = InlineKeyboardButton(text=f"Пройти тест",
        web_app=WebAppInfo(url='https://rawcdn.githack.com/rubix0307/dorenella-bot/20267db75ad528013858f1c93a80f4b43371fd06/media/contest.html'))
    counseling = InlineKeyboardButton(text=f"Консультація",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.counseling.value).pack(),
        )
    accompaniment = InlineKeyboardButton(text=f"Місячний супровід",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.accompaniment.value).pack(),
        )
    accompaniment_back = InlineKeyboardButton(text=f"Назад",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.accompaniment_back.value).pack(),
        )
    feedbacks = InlineKeyboardButton(text=f"Відгуки",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.feedbacks.value).pack(),
        )
    feedbacks_back = InlineKeyboardButton(text=f"Послуги",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.feedbacks_back.value).pack(),
        )
    start = InlineKeyboardButton(text=f"На головну",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.start.value).pack(),
        )
    order_counseling = InlineKeyboardButton(text=f"Записатись",
        callback_data=MenuAction(
            action=Action.counseling_message.value,
            menu=MenuName.order_counseling.value).pack(),
        )
    accompaniment_detail = InlineKeyboardButton(text=f"Що входить у місячне введення?",
        callback_data=MenuAction(
            action=Action.open_menu.value,
            menu=MenuName.accompaniment_detail.value).pack(),
        )
    order_accompaniment = InlineKeyboardButton(text=f"Записатись",
        callback_data=MenuAction(
            action=Action.accompaniment_message.value,
            menu=MenuName.order_accompaniment.value).pack(),
        )


class MenuKeyboard:

    def __init__(self):
        self.builder = InlineKeyboardBuilder()

    def get_start(self):
        self.builder.row(MenuButton.trust.value)
        self.builder.row(MenuButton.services.value, MenuButton.ask_me.value)
        self.builder.row(MenuButton.test.value)
        return self.builder.as_markup()
    def get_services(self) -> InlineKeyboardMarkup:
        self.builder.row(MenuButton.counseling.value)
        self.builder.row(MenuButton.accompaniment.value)
        self.builder.row(MenuButton.feedbacks.value)
        self.builder.row(MenuButton.start.value)
        return self.builder.as_markup()

    def get_trust(self) -> InlineKeyboardMarkup:
        self.builder.row(MenuButton.trust_back.value)
        return self.builder.as_markup()

    def get_test(self) -> InlineKeyboardMarkup:
        self.builder.row(MenuButton.test_url.value)
        self.builder.row(MenuButton.start.value)
        return self.builder.as_markup()

    def get_counseling(self) -> InlineKeyboardMarkup:
        self.builder.row(MenuButton.order_counseling.value)
        self.builder.row(MenuButton.services.value)
        return self.builder.as_markup()

    def get_accompaniment(self) -> InlineKeyboardMarkup:
        self.builder.row(MenuButton.accompaniment_detail.value)
        self.builder.row(MenuButton.services.value)
        return self.builder.as_markup()

    def get_accompaniment_detail(self) -> InlineKeyboardMarkup:
        self.builder.row(MenuButton.order_accompaniment.value)
        self.builder.row(MenuButton.accompaniment_back.value)
        return self.builder.as_markup()

    def get_feedbacks(self):
        self.builder.row(InlineKeyboardButton(text=f"Кейс 1", url='https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTkxNTg5MDE1NDk5ODk5?story_media_id=2921236917353841451&igsh=Y2t0N3lmemk5YTAy'))
        self.builder.row(InlineKeyboardButton(text=f"Кейс 2", url='https://www.instagram.com/s/aGlnaGxpZ2h0OjE4MTk1NjI2MTUyMjMwODIz?story_media_id=2996790458022493684&igsh=MW5tOHc3b3NscmFudg=='))
        self.builder.row(InlineKeyboardButton(text=f"Кейс 3", url='https://www.instagram.com/s/aGlnaGxpZ2h0OjE4MDcwMjE2MzgxMzUxMTcw?story_media_id=3027981169400842098&igsh=MTgxZGFidGNrNDNkNg=='))
        self.builder.row(InlineKeyboardButton(text=f"Кейс 4", url='https://www.instagram.com/s/aGlnaGxpZ2h0OjE4MDA1NTQ1MDI3NTc0ODg3?story_media_id=3033084619117112510&igsh=eDdrNWpncWdjY29t'))
        self.builder.row(InlineKeyboardButton(text=f"Кейс 5", url='https://www.instagram.com/s/aGlnaGxpZ2h0OjE4MDU0NTI3MDI2MzYxODkx?story_media_id=3044653143484528007&igsh=YXp4NjU1ZWYzejBt'))
        self.builder.row(InlineKeyboardButton(text=f"Кейс 6", url='https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTU1MjI2NjczNTY4OTcy?story_media_id=3098782770214155527&igsh=cW5kamx0dm90MHgy'))
        self.builder.row(InlineKeyboardButton(text=f"Кейс 7", url='https://www.instagram.com/s/aGlnaGxpZ2h0OjE4MDA3MjMyNzI1Njc2MDc2?story_media_id=3106767350304392091&igsh=MXR6NmN2anc0dGxpcw=='))
        self.builder.row(InlineKeyboardButton(text=f"Кейс 8", url='https://www.instagram.com/s/aGlnaGxpZ2h0OjE4MDExMjMwNDUwNzEwNTU4?story_media_id=3126385386548158076&igsh=MXU1OWd0eDFsY3dnMg=='))
        self.builder.row(MenuButton.feedbacks_back.value)
        return self.builder.as_markup()

    @staticmethod
    def get_share_contact() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Надіслати номер телефону', request_contact=True)]], resize_keyboard=True)

