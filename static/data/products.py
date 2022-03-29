import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, UserMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_sold = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creator_avatar_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
