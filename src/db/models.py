from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Model(Base):
    __abstract__ = True
    __mapper_args__ = {
        "eager_defaults": True,
    }


class User(Model):
    __tablename__ = "users"

    id = Column(  # noqa: A003
        Integer,
        primary_key=True,
    )
    user_id = Column(
        Integer,
        unique=True,
    )
    blog_user_id = Column(Integer)
    blog_username = Column(Text)
    state_auth = Column(Integer)
