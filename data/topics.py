import datetime
import sqlalchemy
from sqlalchemy import orm, Enum

from .db_session import SqlAlchemyBase
from .my_enum import TopicParentType


class Topic(SqlAlchemyBase):
    __tablename__ = 'topics'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    # forum_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("forums.id"), nullable=False)
    parent_type = sqlalchemy.Column(Enum(TopicParentType), nullable=False)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    author = orm.relationship('User')
    # forum = orm.relationship('Forum')
