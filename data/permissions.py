import sqlalchemy
from sqlalchemy import orm, Column

from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'role_to_permission',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('role_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('roles.id')),
    sqlalchemy.Column('permission_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('permissions.id'))
)

class Permission(SqlAlchemyBase):
    __tablename__ = 'permissions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String)
