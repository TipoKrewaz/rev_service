from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
Sessioncreating = sessionmaker(bind=engine, class_= AsyncSession ,expire_on_commit=False)


class Base(DeclarativeBase):
    pass