from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from config import settings

engine = create_engine(settings.DATABASE_URL)
Sessioncreating = sessionmaker(engine, class_=Session ,expire_on_commit=False)



class Base(DeclarativeBase):
    pass
