from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Furniture(Base):
    __tablename__ = 'furniture'

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)
    characteristic = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)

