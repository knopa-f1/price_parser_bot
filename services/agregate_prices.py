from aiogram.types import BufferedInputFile
from pandas import DataFrame

from db.requests import get_average_items_prices
from services.utils import get_df_as_picture


async def get_average_prices()->BufferedInputFile|None:
    prices = await get_average_items_prices()
    if prices:
        image = await get_df_as_picture(DataFrame(prices))
        return image
