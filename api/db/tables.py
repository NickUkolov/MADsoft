from sqlalchemy import Column, Integer, String

from db.base import Base


class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    image_key = Column(String)
    description = Column(String)