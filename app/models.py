from .database import Base

from sqlalchemy import TIMESTAMP, Column, ForeignKey,Integer,Boolean, SmallInteger,String, text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__='posts'

    id = Column(type_=Integer,primary_key=True,autoincrement=True,nullable=False)
    title = Column(type_=String(100),nullable=False)
    content = Column(type_=String(2000),nullable=True)
    created_at = Column(type_=TIMESTAMP(timezone=True),nullable=False,server_default=text('CURRENT_TIMESTAMP()'))
    updated_at = Column(type_=TIMESTAMP(timezone=True),nullable=False,server_default=text('CURRENT_TIMESTAMP()'))
    published = Column(type_=Boolean,nullable=False,server_default=text('True'))
    user_id =Column(Integer,ForeignKey(column="users.id",ondelete="CASCADE"),nullable=False)

    user = relationship("User", back_populates="posts")

class User(Base):
    __tablename__='users'

    id = Column(type_=Integer,primary_key=True,autoincrement=True,nullable=False)
    first_name = Column(type_=String(200),nullable=False)
    last_name = Column(type_=String(200),nullable=True)
    email_id = Column(type_=String(500),nullable=False)
    password = Column(type_=String(1000),nullable=False)
    created_at = Column(type_=TIMESTAMP(timezone=True),nullable=False,server_default=text('CURRENT_TIMESTAMP()'))
    updated_at = Column(type_=TIMESTAMP(timezone=True),nullable=False,server_default=text('CURRENT_TIMESTAMP()'))

    posts = relationship("Post", back_populates="user")


class Vote(Base):
    __tablename__='votes'

    post_id = Column(Integer,ForeignKey(column="posts.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey(column="users.id",ondelete="CASCADE"),primary_key=True,nullable=False)