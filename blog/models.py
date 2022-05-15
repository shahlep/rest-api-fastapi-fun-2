from sqlalchemy import Column, Integer, String, ForeignKey
from .databases import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blog"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    # https://docs.sqlalchemy.org/en/14/orm/relationship_api.html?highlight=relationship#sqlalchemy.orm.relationship
    content_creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)

    blogs = relationship("Blog", back_populates="content_creator")
