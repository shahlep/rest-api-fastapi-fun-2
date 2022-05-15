from sqlalchemy import Column, Integer, String
from .databases import Base


class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
