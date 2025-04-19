from sqlalchemy import select, func

from db.connection import database
from db.models import Source, ParsedPrice
from services.utils import get_site_address

async def add_objects_to_db(objects:list):
    async with database.session as session:
        [session.add(ob) for ob in objects]
        await session.commit()

async def load_sources(dataframe,
                       chat_id: int) -> None:
    async with database.session as session:
        for _, row in dataframe.iterrows():
            source = await get_source_by_url(row['url'].strip(), session)
            if not source:
                source = Source(
                    chat_id=chat_id,
                    item=row['title'].strip(),
                    url=row['url'].strip(),
                    site=get_site_address(row['url']),
                    xpath=row['xpath'].strip()
                )
                session.add(source)
        await session.commit()

async def get_unparsed_sources():
    async with database.session as session:
        stmt = (
            select(Source)
            .where(Source.parsed_at.is_(None))
            .distinct()
        )
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_source_by_url(url, session):
    stmt = (
        select(Source)
        .where(Source.url == url)
    )
    result = await session.execute(stmt)
    instance = result.scalar_one_or_none()
    return instance

async def get_average_items_prices(**filters):
    async with database.session as session:
        stmt = (
            select(ParsedPrice.item.label("Товар"), ParsedPrice.site.label("Сайт"), func.avg(ParsedPrice.price).label("Средняя цена") )
            .where(**filters).group_by(ParsedPrice.item, ParsedPrice.site)
        )
        result = await session.execute(stmt)
        return result.fetchall()
