import datetime

import settings
from database import Base
from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapper, mapped_column


class BaseInfoMixin:
    id = Column(Integer, primary_key=True)
    # id: Mapper[int] = mapped_column(primary_key=True)
    notes = Column(String(settings.Settings.MAX_NOTES_LEN))
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)



class User(BaseInfoMixin, Base):
    __tablename__ = 'user'

    name = Column(String, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_conflict = Column(Boolean, default=False)
   

    def __repr__(self) -> str:
        return f'User {self.name} -> #{self.id}'
    


class Recipe(BaseInfoMixin, Base):
    __tablename__ = 'recipe'
    
    title = Column(String, nullable=False)
    image = Column(String, nullable=False)
    complexity = Column(String, nullable=False)
    category = Column(String, nullable=False)
    recipe = Column(String, nullable=False)
