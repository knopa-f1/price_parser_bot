from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsCorrectFormat(BaseFilter):
    async def __call__(self, message: Message) -> bool | None:
        document = message.document
        file_format = ""
        if document:
            file_format: str = document.file_name.split('.')[-1]
        if message.document:
            file_format: str = message.document.file_name.split('.')[-1].lower()

        return file_format in ('xls', 'xlsx')
