import logging
import re
from datetime import datetime
from decimal import Decimal

import aiohttp
from parsel import Selector

from db.models import Source, ParsedPrice
from db.requests import get_unparsed_sources, add_objects_to_db

logger = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9",
}

async def fetch_html(url:str) -> str:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 403:
                logger.error("403 ошибка при обращении к %s", url)
            return await response.text()

async def parse_price(url, xpath) -> Decimal|None:
    text = await fetch_html(url)
    selector = Selector(text= text)

    raw_price = selector.xpath(xpath + '/text()').get()
    if raw_price:
        price = re.sub(r"[^\d.,]", "", raw_price).replace(",", ".")
        print(url, price)
        return Decimal(price)

async def get_parsed_prices(sources:list[Source]) -> tuple[list, list]:
    parsed_prices = []
    sources_to_update = []
    for source in sources:
        price = await parse_price(source.url, source.xpath)
        if price:
            parsed_price = ParsedPrice(item=source.item,
                                       site=source.site,
                                       price=price,
                                       source_id=source.id)
            parsed_prices.append(parsed_price)
        source.parsed_at = datetime.now()
        sources_to_update.append(source)
    return parsed_prices, sources_to_update

async def parse_prices_and_load_to_db() -> None:
    sources:list[Source] = await get_unparsed_sources()
    parsed_prices, sources_to_update = await get_parsed_prices(sources)
    parsed_prices.extend(sources_to_update)
    await add_objects_to_db(parsed_prices)
