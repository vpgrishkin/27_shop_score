import os

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_CONFIG = os.getenv("DB_CONFIG")

engine = create_engine(DB_CONFIG)
Session = sessionmaker()
Base = declarative_base(bind=engine)
session = Session(bind=engine)


class Order(Base):
    __tablename__ = 'orders'
    id = Column('id', Integer, primary_key=True)
    created = Column(DateTime)
    confirmed = Column(DateTime)

    def __repr__(self):
        return self.created