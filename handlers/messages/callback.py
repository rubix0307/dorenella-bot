from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile

from config import Action, MenuAction, MenuKeyboard
from handlers.messages.commands import start
from ORM.models import SystemText
from run import dp


@dp.callback_query(MenuAction.filter(F.action == Action.open_menu.value))
async def answer(callback_query: CallbackQuery, callback_data: MenuAction):
    message = callback_query.message

    match callback_data.menu:
        case 'start':
            await start(callback_query.message)

        case 'services':
            caption = await SystemText.objects.aget(menu='services')
            photo = FSInputFile('media/services.jpg')
            await message.answer_photo(
                photo=photo,
                caption=caption.text or None,
                reply_markup=MenuKeyboard().get_services(),
                disable_notification=True,
            )
            await message.delete()

        case 'trust':
            caption = await SystemText.objects.aget(menu='trust')
            await message.edit_caption(
                caption=caption.text.format_map(locals()) or None,
                reply_markup=MenuKeyboard().get_trust(),
            )
        case 'trust_back':
            caption = await SystemText.objects.aget(menu='start')
            await message.edit_caption(
                caption=caption.text.format_map(locals()) or None,
                reply_markup=MenuKeyboard().get_start(),
            )

        case 'test':
            caption = await SystemText.objects.aget(menu='test')
            photo = FSInputFile('media/test.jpg')
            await message.answer_photo(
                photo=photo,
                caption=caption.text or None,
                reply_markup=MenuKeyboard().get_test(),
                disable_notification=True,
            )
            await message.delete()
        case 'counseling':
            caption = await SystemText.objects.aget(menu='counseling')
            photo = FSInputFile('media/counseling.jpg')
            await message.answer_photo(
                photo=photo,
                caption=caption.text.format_map(locals()) or None,
                reply_markup=MenuKeyboard().get_counseling(),
                disable_notification=True,
            )
            await message.delete()

        case 'accompaniment':
            caption = await SystemText.objects.aget(menu='accompaniment')
            photo = FSInputFile('media/accompaniment.jpg')
            await message.answer_photo(
                photo=photo,
                caption=caption.text.format_map(locals()) or None,
                reply_markup=MenuKeyboard().get_accompaniment(),
                disable_notification=True
            )
            await message.delete()

        case 'accompaniment_detail':
            caption = await SystemText.objects.aget(menu='accompaniment_detail')
            await message.edit_caption(
                caption=caption.text.format_map(locals()) or None,
                reply_markup=MenuKeyboard().get_accompaniment_detail(),
            )
        case 'accompaniment_back':
            caption = await SystemText.objects.aget(menu='accompaniment')
            await message.edit_caption(
                caption=caption.text.format_map(locals()) or None,
                reply_markup=MenuKeyboard().get_accompaniment(),
            )

        case 'feedbacks':
            await message.edit_caption(
                caption=None,
                reply_markup=MenuKeyboard().get_feedbacks(),
            )
            await callback_query.answer()

        case 'feedbacks_back':
            await message.edit_caption(
                caption=None,
                reply_markup=MenuKeyboard().get_services(),
            )
            await callback_query.answer()
