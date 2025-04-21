import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config_data.constants import PARSER_INTERVAL
from services.parse_prices import parse_prices_and_load_to_db

logger = logging.getLogger(__name__)

async def main():
    scheduler: AsyncIOScheduler = AsyncIOScheduler()

    scheduler.add_job(parse_prices_and_load_to_db, IntervalTrigger(seconds=PARSER_INTERVAL))
    scheduler.start()
    await asyncio.Event().wait()

asyncio.run(main())
