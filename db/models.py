from datetime import datetime

from sqlalchemy import BigInteger, String, TIMESTAMP, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column

from db.base_model import Base


class Source(Base): # pylint: disable=too-few-public-methods
    __tablename__ = 'sources'

    item:      Mapped[str] = mapped_column(String, nullable=False)
    url:       Mapped[str] = mapped_column(String, nullable=False)
    xpath:     Mapped[str] = mapped_column(String, nullable=False)
    site:      Mapped[str] = mapped_column(String, nullable=False)
    chat_id:   Mapped[int] = mapped_column(BigInteger, nullable=False)

    parsed_at: Mapped[datetime|None] = mapped_column(TIMESTAMP(timezone=False), nullable=True)

class ParsedPrice(Base): # pylint: disable=too-few-public-methods
    __tablename__ = 'parsed_prices'

    item:      Mapped[str] = mapped_column(String, nullable=False)
    site:       Mapped[str] = mapped_column(String, nullable=False)
    price:     Mapped[float | None] = mapped_column(Float, nullable=True)
    source_id: Mapped[int | None] = mapped_column(BigInteger,
                                                    ForeignKey('sources.id'))
