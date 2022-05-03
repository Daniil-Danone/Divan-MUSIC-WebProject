import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
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
    path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    local_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    icon_file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    preview_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    creator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))

    creator = orm.relationship("User", backref="Product", primaryjoin="User.id == Product.creator_id")
