from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Furniture(Base):
    __tablename__ = 'furniture'

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)
    characteristic = Column(String(500), nullable=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)

    # ✅ Добавляем связь с ProductImage
    images = relationship("ProductImage", back_populates="furniture", lazy="joined")

class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(255), nullable=False)

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    furniture_id = Column(Integer, ForeignKey("furniture.id"))
    image_id = Column(Integer, ForeignKey("image.id"))

    furniture = relationship("Furniture", back_populates="images")
    image = relationship("Image")

