import pandas as pd

from config_data.constants import COLUMNS
from db.requests import load_sources
from lexicon.lexicon import LEXICON_RU
from services.utils import get_df_as_picture


async def upload_file_to_db(filename, chat_id:int) -> pd.DataFrame:
    dataframe = pd.read_excel(filename)

    if not COLUMNS.issubset(dataframe.columns):
        raise ValueError(LEXICON_RU["upload_file_wrong_columns"])

    await load_sources(dataframe, chat_id)
    return await get_df_as_picture(dataframe)
