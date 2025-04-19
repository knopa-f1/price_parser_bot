import os
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Document, Message, CallbackQuery

from config_data.constants import TEMP_DIR

from filters.filters import IsCorrectFormat
from lexicon.lexicon import LEXICON_RU

from keyboards.inline_keyboards import start_keyboard
from services.agregate_prices import get_average_prices

from services.upload_file_service import upload_file_to_db
from states.states import UploadExcel

router = Router()

KEYBOARD = start_keyboard()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=KEYBOARD
    )

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

@router.callback_query(F.data == 'button_upload')
async def process_button_upload(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU['upload_file_text'])
    await state.set_state(UploadExcel.waiting_for_file)

@router.message(StateFilter(UploadExcel.waiting_for_file), IsCorrectFormat())
async def process_user_send_file(message: Message, bot: Bot, state: FSMContext):
    await message.answer(text=LEXICON_RU['upload_file_wait'])
    doc: Document = message.document
    timestamp = datetime.timestamp(datetime.now())
    filename = f"{TEMP_DIR}file_{message.chat.id}_{timestamp}.xlsx"
    await bot.download(file=doc.file_id, destination=filename)

    try:
        image = await upload_file_to_db(filename, message.chat.id)
        await (message.answer_photo(photo=image,
                                    caption=f'{LEXICON_RU["upload_file_success"]}'))
    except Exception as er:
        await message.answer(f"Ошибка: {er}", keyboard=KEYBOARD)
    finally:
        os.remove(filename)
    await state.clear()

@router.message(StateFilter(UploadExcel.waiting_for_file), ~IsCorrectFormat())
async def process_user_send_file_warning(message: Message):
    await message.answer(
        text=LEXICON_RU['upload_file_error'],
        reply_markup=KEYBOARD
    )

@router.callback_query(F.data == 'button_avg_prices')
async def process_button_av_prices(callback: CallbackQuery):
    image = await get_average_prices()
    if image:
        await (callback.message.answer_photo(photo=image,
                                         caption=f'{LEXICON_RU["avg_prices_success"]}'))
    else:
        await callback.message.answer(
            text=LEXICON_RU['avg_prices_empty'],
            reply_markup=KEYBOARD
        )
