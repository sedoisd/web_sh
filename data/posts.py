import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    created_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now(), nullable=False)
    modified_data = sqlalchemy.Column(sqlalchemy.DateTime, default=None)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    topic_id =  sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"), nullable=False)

    # author = orm.relationship('User')
    topic = orm.relationship('Topic')