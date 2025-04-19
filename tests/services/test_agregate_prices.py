from unittest import mock
from unittest.mock import patch, AsyncMock

import pytest

from services.agregate_prices import get_average_prices


@patch('services.agregate_prices.get_df_as_picture', new_callable=AsyncMock)
@patch('services.agregate_prices.get_average_items_prices', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_average_prices_image(mock_get_average_items_prices, mock_get_df_as_picture):
    mock_data = [{"item": "book", "price": 10}]
    mock_get_average_items_prices.return_value = mock_data
    mock_get_df_as_picture.return_value = mock.Mock()
    result = await get_average_prices()

    mock_get_average_items_prices.assert_called_once()
    mock_get_df_as_picture.assert_called_once()
    assert result == mock_get_df_as_picture.return_value

@patch('services.agregate_prices.get_df_as_picture', new_callable=AsyncMock)
@patch('services.agregate_prices.get_average_items_prices', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_average_prices_empty_prices(mock_get_average_items_prices, mock_get_df_as_picture):
    mock_data = []
    mock_get_average_items_prices.return_value = mock_data
    await get_average_prices()

    mock_get_average_items_prices.assert_called_once()
    mock_get_df_as_picture.assert_not_called()
