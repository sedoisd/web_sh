import datetime
import sqlalchemy
from sqlalchemy import orm, Enum

from .db_session import SqlAlchemyBase
from .my_enum import ForumParentType


class Forum(SqlAlchemyBase):
    __tablename__ = 'forums'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    # category_id =  sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"), nullable=False)
    parent_type = sqlalchemy.Column(Enum(ForumParentType), nullable=False)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    author = orm.relationship('User')
    # category = orm.relationship('Category')
