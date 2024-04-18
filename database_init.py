from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated
from config_reader import config


engine = create_async_engine(
    url=config.database_url,
    echo=True
)

session_factory = async_sessionmaker(engine)

str_255 = Annotated[str, 255]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_255: String(255)
    }
