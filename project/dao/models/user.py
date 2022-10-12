from marshmallow import Schema, fields

from project.setup.db import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String #todo присвоить уникальность
    password = fields
    name = fields.String()
    surname = fields.String()
    favorite_genre = fields.String()
