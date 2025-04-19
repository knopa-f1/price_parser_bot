from aiogram.fsm.state import StatesGroup, State

class UploadExcel(StatesGroup):# pylint: disable=too-few-public-methods
    waiting_for_file = State()
