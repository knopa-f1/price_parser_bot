from decimal import Decimal
from datetime import datetime
from unittest.mock import patch

import pytest

from services.parse_prices import get_parsed_prices, parse_prices_and_load_to_db
from db.models import Source, ParsedPrice

@patch("services.parse_prices.parse_price")
@pytest.mark.asyncio
async def test_get_parsed_prices(mock_parse_price):
    mock_parse_price.return_value = Decimal("999.99")
    source = Source(id=1, item="Item", site="Site", url="http://test", xpath="//price")
    result, updated = await get_parsed_prices([source])

    assert len(result) == 1
    assert isinstance(result[0], ParsedPrice)
    assert len(updated) == 1
    assert isinstance(updated[0].parsed_at, datetime)

@patch("services.parse_prices.get_unparsed_sources")
@patch("services.parse_prices.get_parsed_prices")
@patch("services.parse_prices.add_objects_to_db")
@pytest.mark.asyncio
async def test_parse_prices_and_load_to_db(mock_add, mock_get_parsed, mock_get_sources):
    mock_source = Source(id=1, item="Item", site="Site", url="http://test", xpath="//price")
    mock_get_sources.return_value = [mock_source]
    parsed_price = ParsedPrice(item="Item", site="Site", price=Decimal("10.0"), source_id=1)
    mock_get_parsed.return_value = ([parsed_price], [mock_source])

    await parse_prices_and_load_to_db()

    mock_add.assert_called_once()
    all_items = mock_add.call_args[0][0]
    assert parsed_price in all_items
    assert mock_source in all_items
