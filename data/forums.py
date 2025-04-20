import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Forum(SqlAlchemyBase):
    __tablename__ = 'forums'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    category_id =  sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"), nullable=False)

    author = orm.relationship('User')
    category = orm.relationship('User')
