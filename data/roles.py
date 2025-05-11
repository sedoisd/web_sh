import sqlalchemy
from sqlalchemy import orm, Column

from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'role_to_user',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('role_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('roles.id')),
    sqlalchemy.Column('user_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)

class Role(SqlAlchemyBase):
    __tablename__ = 'roles'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    title_on_russian = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String)

    permissions = orm.relationship("Permission",
                                  secondary="role_to_permission",
                                  backref="role")