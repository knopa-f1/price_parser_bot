import os
from datetime import datetime
from urllib.parse import urlparse
import dataframe_image as dfi
from aiogram.types import BufferedInputFile

from config_data.constants import TEMP_DIR


def get_site_address(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.netloc:
        return parsed_url.netloc
    elif parsed_url.path:
        return parsed_url.path.split('/')[0]
    return ''

async def get_df_as_picture(df):
    timestamp = datetime.timestamp(datetime.now())
    filename = f"{TEMP_DIR}df_{timestamp}.png"
    await dfi.export_async(df, filename)

    with open(filename, "rb") as f:
        img_bytes = f.read()

    os.remove(filename)

    return BufferedInputFile(img_bytes, filename="df.png")
