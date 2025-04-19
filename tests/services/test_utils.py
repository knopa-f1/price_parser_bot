from unittest.mock import patch, AsyncMock

import pytest
import pandas as pd
from unittest import mock

from services.utils import get_site_address, get_df_as_picture


def test_get_site_address():
    url = "http://test.com/page"
    expected = "test.com"
    assert get_site_address(url) == expected

@patch("builtins.open", new_callable=mock.mock_open)
@patch('services.utils.os.remove')
@patch('services.utils.dfi.export_async', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_df_as_picture(mock_export, mock_remove, mock_open): # pylint: disable=unused-argument
    test_df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})

    await get_df_as_picture(test_df)

    mock_export.assert_called_once()
    mock_remove.assert_called_once()
