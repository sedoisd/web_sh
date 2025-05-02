import datetime
import sqlalchemy
from sqlalchemy import orm, Enum

from .db_session import SqlAlchemyBase
from .my_enum import CategoryParentType


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    # group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"), nullable=False)
    parent_type = sqlalchemy.Column(Enum(CategoryParentType), nullable=False)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    author = orm.relationship('User')
    # group = orm.relationship('Group')
