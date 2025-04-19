from unittest.mock import patch, AsyncMock

import pytest
import pandas as pd

from services.upload_file_service import upload_file_to_db
from lexicon.lexicon import LEXICON_RU


@patch("services.upload_file_service.get_df_as_picture", new_callable=AsyncMock)
@patch("services.upload_file_service.load_sources", new_callable=AsyncMock)
@patch("services.upload_file_service.pd.read_excel")
@pytest.mark.asyncio
async def test_upload_file_to_db_valid(mock_read_excel, mock_load_sources, mock_get_picture):
    df = pd.DataFrame(columns=["title", "url", "xpath"])
    mock_read_excel.return_value = df
    mock_get_picture.return_value = "image"

    result = await upload_file_to_db("fake.xlsx", chat_id=123)

    mock_read_excel.assert_called_once_with("fake.xlsx")
    mock_load_sources.assert_called_once_with(df, 123)
    mock_get_picture.assert_called_once_with(df)
    assert result == "image"

@pytest.mark.asyncio
@patch("services.upload_file_service.pd.read_excel")
async def test_upload_file_to_db_invalid_columns(mock_read_excel):
    df = pd.DataFrame(columns=["url", "xpath"])
    mock_read_excel.return_value = df

    with pytest.raises(ValueError, match=LEXICON_RU["upload_file_wrong_columns"]):
        await upload_file_to_db("fake.xlsx", chat_id=123)
